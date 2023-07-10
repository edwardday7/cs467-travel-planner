from flask import render_template, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, db
from app.models.models import Trip, User

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/trips')
@jwt_required()
def users():
    username = get_jwt_identity()
    trips = db.session.execute(db.select(Trip).join_from(User, Trip).where(User.username == username)).scalars()
    return render_template('trips.html', trips=trips)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200
