from flask import render_template, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, db
from app.models.models import Trip, User, Experience, Follower
from sqlalchemy import desc
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
def map(lat, long, name):
    m = folium.Map()
    coordinate = (lat, long)
    folium.Marker(coordinate, popup=name).add_to(m)
    m.get_root().width = "500px"
    m.get_root().height = "300px"
    iframe = m.get_root()._repr_html_()
    return render_template("map.html", iframe = iframe)

@app.route('/trips')
@jwt_required()
def users():
    username = get_jwt_identity()
    trips = db.session.execute(db.select(Trip).join_from(User, Trip).where(User.username == username)).scalars()
    return render_template('trips.html', trips=trips)


@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200
