import uuid
from flask import make_response, redirect, render_template, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, db, container_client
from app.models.models import Experience, Rating
from sqlalchemy import desc, or_
from sqlalchemy.sql import func
import operator

@app.route('/experiences', methods=['GET'])
def experiences():
    search = request.args.get('q')
    sort = request.args.get('sort')

    if search:
        experiences = Experience.query.filter(or_(Experience.title.contains(search), Experience.description.contains(search)))
    else:
        experiences = Experience.query

    exp_id_ratings_map = {}     # In order to find average rating for each experience ID
    ratings = Rating.query.with_entities(Rating.experience_id, func.avg(Rating.rating)).group_by(Rating.experience_id)
    for rating in ratings:
        experience_id = rating[0]
        average_rating = rating[1]
        exp_id_ratings_map[experience_id] = average_rating

    experiences = experiences.all()
    experiences_list = []
    for experience in experiences:
        average_ratings = "-"
        if experience.id in exp_id_ratings_map:
            average_ratings = exp_id_ratings_map[experience.id]
            average_ratings = round(average_ratings, 2)
        exp = {
            "id": experience.id,
            "user_username": experience.user_username,
            "title": experience.title,
            "description": experience.description,
            "latitude": experience.latitude,
            "longitude": experience.longitude,
            "state": experience.state,
            "country": experience.country,
            "image": experience.image,
            "time_created": experience.time_created,
            "rating": average_ratings
        }
        experiences_list.append(exp)

    #this is borked
    if sort == 'highest_rating':
        experiences_list.sort(key=operator.itemgetter('rating'), reverse=True)
    elif sort == 'lowest_rating':
        experiences_list.sort(key=operator.itemgetter('rating'))

    return render_template('experiences.html', experiences=experiences_list)


@app.route('/experience/<int:experience_id>', methods=['GET'])
def experience_detail(experience_id):
    experience = Experience.query.get_or_404(experience_id)
    return render_template('experience_detail.html', experience=experience)


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
            latitude=float(request.form.get('latitude')),
            longitude=float(request.form.get('longitude')),
            state=request.form.get('state'),
            country=request.form.get('country'),
            image=upload_file(request.files.get('file')).url  # blob_client.url
        )
        
        db.session.add(new_experience)
        db.session.commit()

        return redirect('/')
    
def upload_file(image):

    return container_client.upload_blob(image.filename + str(uuid.uuid4()), image)