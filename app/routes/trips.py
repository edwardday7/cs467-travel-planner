import uuid
from flask import make_response, redirect, render_template, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, db, container_client
from app.models.models import Experience, Rating, Trip, User, Follower, TripExperience
from sqlalchemy import desc, or_
from sqlalchemy.sql import func
from sqlalchemy import and_


@app.route('/trips')
@jwt_required()
def trips():
    username = get_jwt_identity()
    user_trips = db.session.execute(db.select(Trip).join_from(User, Trip).where(User.username == username)).scalars()
    return render_template('trips.html', trips=user_trips)


@app.route('/trips/new', methods=["GET", "POST"])
@jwt_required()
def create_trip():
    if request.method == "GET":
        current_user = get_jwt_identity()

        return render_template('create_trip.html', current_user=current_user)
    else:
        trip_name = request.form.get('trip_name')

        trip = Trip(
            user_username=get_jwt_identity(),
            trip_name=trip_name,
        )

        db.session.add(trip)
        db.session.commit()

        return redirect('/trips')


@app.route('/trips/<int:trip_id>', methods=['GET'])
@jwt_required()
def trip_detail(trip_id):
    current_user = get_jwt_identity()

    all_experiences = (db.session.query(TripExperience, Trip, Experience)
                       .join(Trip, Trip.id == TripExperience.trip_id)
                       .join(Experience, TripExperience.experience_id == Experience.id)
                       .filter(and_(TripExperience.trip_id == trip_id, Trip.user_username == current_user))).all()

    experiences_object_list = []

    exp_id_ratings_map = {}  # In order to find average rating for each experience ID
    ratings = Rating.query.with_entities(Rating.experience_id, func.avg(Rating.rating)).group_by(Rating.experience_id)
    for rating in ratings:
        experience_id = rating[0]
        average_rating = rating[1]
        exp_id_ratings_map[experience_id] = average_rating

    for all_experience in all_experiences:
        trip = all_experience[1]
        experience = all_experience[2]

        average_ratings = "-"
        if experience.id in exp_id_ratings_map:
            average_ratings = exp_id_ratings_map[experience.id]
            average_ratings = round(average_ratings, 2)

        experiences_object = {
            "trip_id": trip.id,
            "experience_id": experience.id,
            "title": experience.title,
            "description": experience.description,
            "rating": average_ratings
        }
        experiences_object_list.append(experiences_object)

    return render_template('trip_detail.html', experiences=experiences_object_list, trip_id=trip_id)


@app.route('/trips/<int:trip_id>/add/experience', methods=["GET", "POST"])
@jwt_required()
def trip_add_experience(trip_id):
    if request.method == "GET":

        trip = Trip.query.filter(Trip.id == trip_id).first()
        trip_name = trip.trip_name

        # In order to find not selected experiences for the trip to show in the dropdown
        current_user = get_jwt_identity()

        trip_experiences = (db.session.query(TripExperience, Trip, Experience)
                           .join(Trip, Trip.id == TripExperience.trip_id)
                           .join(Experience, TripExperience.experience_id == Experience.id)
                           .filter(and_(TripExperience.trip_id == trip_id, Trip.user_username == current_user))).all()

        already_added_experiences_list = []

        for trip_experience in trip_experiences:
            experience = trip_experience[2]
            already_added_experiences_list.append(experience.id)

        experiences = []
        all_experiences = db.session.query(Experience).all()
        for all_experience in all_experiences:
            experience_id = all_experience.id
            if experience_id not in already_added_experiences_list:
                experiences.append(all_experience)

        return render_template('trip_add_experience.html', trip_id=trip_id, trip_name=trip_name, experiences=experiences)
    else:
        experience_title = request.form.get('experience_title')
        experience_id = ""
        experience = Experience.query.filter(Experience.title == experience_title).first()
        if experience:
            experience_id = experience.id

        trip_experience = TripExperience(
            trip_id=trip_id,
            experience_id=experience_id,
        )

        db.session.add(trip_experience)
        db.session.commit()

        return redirect(f'/trips/{trip_id}')