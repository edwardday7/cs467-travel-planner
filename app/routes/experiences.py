import uuid
from flask import make_response, redirect, render_template, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from geoalchemy2 import WKTElement
from app import app, db, container_client
from app.models.models import Experience, Rating
from sqlalchemy import desc, or_
import os

from sqlalchemy.sql import func

@app.route('/experiences', methods=['GET'])
def experiences():
    
    mapbox_token = os.environ.get("MAPBOX_TOKEN")
    search = request.args.get('q')
    sort = request.args.get('sort')

    if search:
        experiences = db.session.query(Experience, func.avg(Rating.rating).label('average_rating')).\
                      outerjoin(Rating, Experience.id == Rating.experience_id).\
                      group_by(Experience.id).\
                      filter(or_(Experience.title.contains(search), Experience.description.contains(search)))
    else:
        experiences = db.session.query(Experience, func.avg(Rating.rating).label('average_rating')).\
                      outerjoin(Rating, Experience.id == Rating.experience_id).\
                      group_by(Experience.id)
    if sort == 'highest_rating':
        experiences = experiences.order_by(db.desc('average_rating'))
    elif sort == 'lowest_rating':
        experiences = experiences.order_by('average_rating')

    experiences = experiences.all()

    experiences_data = []
    for experience, average_rating in experiences:
        experiences_data.append({
            'id': experience.id,
            'title': experience.title,
            'description': experience.description,
            'latitude': experience.latitude,
            'longitude': experience.longitude,
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
            coordinates=WKTElement(f'POINT({float(request.form.get("latitude"))} {float(request.form.get("longitude"))})'),
            state=request.form.get('state'),
            country=request.form.get('country'),
            image=upload_file(request.files.get('file')).url  # blob_client.url
        )
        
        db.session.add(new_experience)
        db.session.commit()

        return redirect('/')
    
def upload_file(image):
    return container_client.upload_blob(image.filename + str(uuid.uuid4()), image)