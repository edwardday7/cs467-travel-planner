from flask import render_template, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, db
from app.models.models import Trip, User, Experience, Follower
from sqlalchemy import desc, or_
from statistics import mean
import folium

@app.route('/')
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    
    new_exp = db.session.execute(db.select(Experience)
                                         .order_by(Experience.time_created.desc())).scalars()

    follower_exp = db.session.execute(db.select(Experience)
                                   .join(Follower, Follower.follower_username == Experience.user_username)).scalars()

    if not current_user:
        return render_template('home.html', experiences=new_exp, current_user = False)
    else:
       return render_template('home.html', experiences=new_exp, f_exp = follower_exp, current_user = True)

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

@app.route('/experiences', methods=['GET'])
def experiences():
    search = request.args.get('q')
    sort = request.args.get('sort')
    
    if search:
        experiences = Experience.query.filter(or_(Experience.title.contains(search), Experience.description.contains(search)))
    else:
        experiences = Experience.query

    if sort == 'highest_rating':
        experiences = experiences.order_by(Experience.rating.desc())
    elif sort == 'lowest_rating':
        experiences = experiences.order_by(Experience.rating.asc())

    experiences = experiences.all()

    return render_template('experiences.html', experiences=experiences)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200
