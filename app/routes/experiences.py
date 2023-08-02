from collections import defaultdict
import json
import requests
import uuid
from flask import flash, make_response, redirect, render_template, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from geoalchemy2 import WKTElement
from geoalchemy2.functions import ST_DWithin, ST_Transform, ST_SetSRID, ST_Point
from app import app, db, container_client
from app.models.models import Experience, Rating
from sqlalchemy import desc, or_, func
from geoalchemy2.shape import to_shape
import os
from sqlalchemy.sql import func, text

@app.route('/experiences', methods=['GET'])
def experiences():
    mapbox_token = os.environ.get("MAPBOX_TOKEN")
    search_keyword = request.args.get('keyword')
    search_radius = request.args.get('radius')
    search_latitude = request.args.get('latitude')
    search_longitude = request.args.get('longitude')
    search_state = request.args.get('state')
    search_star = request.args.get('star')

    sort = request.args.get('sort')

    experiences = db.session.query(Experience, func.avg(Rating.rating).label('average_rating'), func.ST_AsGeoJSON(Experience.coordinates).label('coordinates'))\
        .outerjoin(Rating, Experience.id == Rating.experience_id).group_by(Experience.id)

    if search_keyword:
        experiences = experiences.filter(or_(Experience.title.contains(search_keyword), Experience.description.contains(search_keyword)))

    if search_state:
        experiences = experiences.filter(Experience.state.ilike(search_state))

    if search_latitude and search_longitude and search_radius:
        search_radius_meters = float(search_radius) * 1609.344  # SRID 4326 uses meters, so we must convert miles to meters

        # Calculate the distance between our search and the coordinates
        distance = func.ST_Distance(
            func.ST_GeomFromText(f'POINT({search_latitude} {search_longitude})', 4326),
            Experience.coordinates
        )

        # If the experience is within our radius
        experiences = experiences.filter(distance <= search_radius_meters)
    
    if search_star:
        search_star = int(search_star)
        experiences = experiences.having(db.func.floor(db.func.avg(Rating.rating)) == search_star)

    if sort == 'highest_rating' or sort is None:
        experiences = experiences.order_by(db.desc('average_rating'))
    elif sort == 'lowest_rating':
        experiences = experiences.order_by('average_rating')

    experiences = experiences.all()

    experiences_data = []
    for experience, average_rating, coordinates in experiences:
        experiences_data.append({
            'id': experience.id,
            'title': experience.title,
            'description': experience.description,
            'coordinates': json.loads(coordinates),
            'average_rating': average_rating
    })
        
    return render_template('experiences.html', experiences=experiences_data, mapbox_token=mapbox_token, to_shape=to_shape)

@app.route('/experience/<int:experience_id>', methods=['GET'])
def experience_detail(experience_id):
    open_weather_token= os.environ.get("OPEN_WEATHER_TOKEN")

    experience = Experience.query.get_or_404(experience_id)

    latitude = to_shape(experience.coordinates).y
    longitude = to_shape(experience.coordinates).x

    lon = latitude
    lat = longitude

    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={open_weather_token}"
    response = requests.get(forecast_url)
    forecast_data = response.json()

    #error checking
    if forecast_data.get('cod') != '200' or 'list' not in forecast_data:
        forecast_data = None
        daily_averages = None
    else:
        daily_temps = defaultdict(list)
        daily_icons = defaultdict(list)
        for day_data in forecast_data['list']:
            date = day_data['dt_txt'][:10]
            temp_kelvin = day_data['main']['temp']
            temp_fahrenheit = (temp_kelvin - 273.15) * 9/5 + 32
            daily_temps[date].append(temp_fahrenheit)
            daily_icons[date].append(day_data['weather'][0]['icon'])

        def is_numeric(n):
            try:
                float(n)
                return True
            except ValueError:
                return False

        daily_averages = {
            date: {
                'temp': round(sum(temps)/len(temps), 2) if all(is_numeric(temp) for temp in temps) else 'No data',
                'icon': max(set(icons), key=icons.count) if icons else 'No data'
            }
            for date, temps, icons in zip(daily_temps.keys(), daily_temps.values(), daily_icons.values())
        }

    nearby_experiences = experience.get_nearby_experiences()
    ratings = Rating.query.filter_by(experience_id=experience_id).all()
    average_rating = round(sum([rating.rating for rating in ratings]) / len(ratings), 1) if ratings else "No rating"
    
    return render_template('experience_detail.html', experience=experience, average_rating=average_rating, 
                           nearby_experiences=nearby_experiences, daily_averages=daily_averages, 
                           to_shape=to_shape, open_weather_token=open_weather_token)

@app.route('/experiences/new', methods=["GET", "POST"])
@jwt_required()
def create_experience():
    if request.method == "GET":
        return render_template('create_experience.html')
    else:
        new_experience = Experience(
            user_username=get_jwt_identity(),
            title=request.form.get('title'),
            description=request.form.get('description'),
            coordinates=WKTElement(f'POINT({float(request.form.get("latitude"))} {float(request.form.get("longitude"))})', srid=4326),
            state=request.form.get('state'),
            country=request.form.get('country'),
            image=upload_file(request.files.get('file')).url  # blob_client.url
        )
        
        db.session.add(new_experience)
        db.session.commit()

        return redirect('/')

def upload_file(image):
    return container_client.upload_blob(image.filename + str(uuid.uuid4()), image)