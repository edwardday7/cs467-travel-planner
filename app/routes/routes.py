from flask import render_template, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, db
from app.models.models import Trip, User, Experience, Follower, Rating
from sqlalchemy import desc
from statistics import mean
import folium
from sqlalchemy import and_

@app.route('/')
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    # print(current_user)

    new_exp = db.session.execute(db.select(Experience)
                                         .order_by(Experience.time_created.desc())).scalars()

    follower_exp = db.session.execute(db.select(Experience)
                                      .join(Follower, and_(Follower.follower_username == Experience.user_username,
                                                           Follower.user_username == current_user))).scalars()

    # exp_rating = db.session.execute(db.select(Experience)
    #                                   .join(Rating, Rating.experience_id == Experience.id)).scalars()

    ratings = db.session.execute(db.select(Rating)).scalars()

    total_ratings_number_of_ratings_map_by_experience_id = {}    # experience_id is the key and value is an array where first element is total ratings sum, second element is number of ratings and third element is average rating round to decimal point.
    rated_users_experience_id_map = {}                           # experience_id is the key and value is the users who rated that experience

    for rating in ratings:
        # print("experience_id :", rating.experience_id)
        # print("username :", rating.username)
        # print("rating :", rating.rating)
        if rating.experience_id not in total_ratings_number_of_ratings_map_by_experience_id:
            total_ratings_number_of_ratings_map_by_experience_id[rating.experience_id] = [0, 0]
            rated_users_experience_id_map[rating.experience_id] = []
        rated_users_experience_id_map[rating.experience_id].append(rating.username)
        ratings_sum = total_ratings_number_of_ratings_map_by_experience_id[rating.experience_id][0] + rating.rating
        number_of_ratings = total_ratings_number_of_ratings_map_by_experience_id[rating.experience_id][1] + 1
        new_arr = [ratings_sum, number_of_ratings]
        total_ratings_number_of_ratings_map_by_experience_id[rating.experience_id] = new_arr

    # print("rated_users_experience_id_map :", rated_users_experience_id_map)

    for key,value in total_ratings_number_of_ratings_map_by_experience_id.items():
        average_rating = 0
        if value[1] > 0:
            average_rating = value[0]/value[1]
            average_rating = round(average_rating)
        total_ratings_number_of_ratings_map_by_experience_id[key].append(average_rating)

    # print("total_ratings_number_of_ratings_map_by_experience_id :", total_ratings_number_of_ratings_map_by_experience_id)

    if not current_user:
        return render_template('index.html')
    else:
       return render_template('home.html', experiences=new_exp, f_exp = follower_exp, current_user = True,
                              current_username=current_user,
                              ratings_map=total_ratings_number_of_ratings_map_by_experience_id,
                              rated_users_experience_id_map=rated_users_experience_id_map)

@app.route('/map/<float:lat>/<long>/<string:name>')
@jwt_required(optional=True)
def map(lat, long, name):
    current_user = bool(get_jwt_identity())
    m = folium.Map()
    coordinate = (lat, long)
    folium.Marker(coordinate, popup=name).add_to(m)
    m.get_root().width = "500px"
    m.get_root().height = "300px"
    iframe = m.get_root()._repr_html_()
    return render_template("map.html", iframe = iframe, current_user = current_user)


@app.route('/trips')
@jwt_required()
def users():
    username = get_jwt_identity()
    trips = db.session.execute(db.select(Trip).join_from(User, Trip).where(User.username == username)).scalars()
    return render_template('trips.html', trips=trips)


@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/index')
def index():
    return render_template('index.html')




