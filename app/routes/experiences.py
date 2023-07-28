import json
import uuid
from flask import make_response, redirect, render_template, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from geoalchemy2 import WKTElement
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

    sort = request.args.get('sort')

    experiences = db.session.query(Experience, func.avg(Rating.rating).label('average_rating'), func.ST_AsGeoJSON(Experience.coordinates).label('coordinates'))\
        .outerjoin(Rating, Experience.id == Rating.experience_id).group_by(Experience.id)

    if search_keyword:
        experiences = experiences.filter(or_(Experience.title.contains(search_keyword), Experience.description.contains(search_keyword)))

    if search_latitude and search_longitude and search_radius:
        search_radius_meters = float(search_radius) * 1609.344  # SRID 4326 uses meters, so we must convert miles to meters

        # Calculate the distance between our search and the coordinates
        distance = func.ST_Distance(
            func.ST_GeomFromText(f'POINT({search_latitude} {search_longitude})', 4326),
            Experience.coordinates
        )

        # If the experience is within our radius
        experiences = experiences.filter(distance <= search_radius_meters)

    if sort == 'highest_rating':
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

    return render_template('experiences.html', experiences=experiences_data, mapbox_token=mapbox_token)


@app.route('/experience/<int:experience_id>', methods=['GET'])
def experience_detail(experience_id):
    experience = Experience.query.get_or_404(experience_id)
    return render_template('experience_detail.html', experience=experience, to_shape=to_shape)

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