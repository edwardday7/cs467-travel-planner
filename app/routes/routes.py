from flask import render_template, jsonify, request, redirect
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, db
from app.models.models import Trip, User, Experience, Follower, Rating
from sqlalchemy import desc, or_
from statistics import mean
import folium
from sqlalchemy import and_
from geoalchemy2.shape import to_shape

@app.route('/')
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()

    new_exp = db.session.execute(db.select(Experience)
                                         .order_by(Experience.time_created.desc())).scalars()
    
    query = db.session.execute(db.select(Follower.follower_username)
                                   .filter(Follower.user_username == current_user)).scalars()
    
    following =[]

    for followers in query:
        following.append(followers)


    follower_exp = db.session.execute(db.select(Experience)
                                      .join(Follower, and_(Follower.follower_username == Experience.user_username,
                                                           Follower.user_username == current_user))).scalars()


    ratings = db.session.execute(db.select(Rating)).scalars()

    total_ratings_number_of_ratings_map_by_experience_id = {}    # experience_id is the key and value is an array where first element is total ratings sum, second element is number of ratings and third element is average rating round to decimal point.
    rated_users_experience_id_map = {}                           # experience_id is the key and value is the users who rated that experience

    for rating in ratings:
        if rating.experience_id not in total_ratings_number_of_ratings_map_by_experience_id:
            total_ratings_number_of_ratings_map_by_experience_id[rating.experience_id] = [0, 0]
            rated_users_experience_id_map[rating.experience_id] = []
        rated_users_experience_id_map[rating.experience_id].append(rating.username)
        ratings_sum = total_ratings_number_of_ratings_map_by_experience_id[rating.experience_id][0] + rating.rating
        number_of_ratings = total_ratings_number_of_ratings_map_by_experience_id[rating.experience_id][1] + 1
        new_arr = [ratings_sum, number_of_ratings]
        total_ratings_number_of_ratings_map_by_experience_id[rating.experience_id] = new_arr

    for key,value in total_ratings_number_of_ratings_map_by_experience_id.items():
        average_rating = 0
        if value[1] > 0:
            average_rating = value[0]/value[1]
            average_rating = round(average_rating)
        total_ratings_number_of_ratings_map_by_experience_id[key].append(average_rating)

    if not current_user:
        return render_template('index.html')
    else:
       return render_template('home.html', experiences=new_exp, f_exp = follower_exp, current_user = True,
                              current_username=current_user,
                              ratings_map=total_ratings_number_of_ratings_map_by_experience_id,
                              rated_users_experience_id_map=rated_users_experience_id_map, 
                              following =following,
                              to_shape=to_shape)

@app.route('/unfollow/<name>')
@jwt_required(optional=True)
def unfollow(name):
    current_user = get_jwt_identity()
    unfollow_user = db.session.query(Follower).filter_by(user_username=current_user, follower_username=name)
    unfollow_user.delete()
    db.session.commit()
    return redirect('/')

@app.route('/follow/<name>')
@jwt_required(optional=True)
def follow(name):
    current_user = get_jwt_identity()
    follow_user = Follower(user_username=current_user, follower_username=name)
    db.session.add(follow_user)
    db.session.commit()
    return redirect('/')


@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

