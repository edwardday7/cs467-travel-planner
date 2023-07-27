from app import db
from geoalchemy2 import Geometry

class User(db.Model):
    username = db.Column(db.String(255), primary_key=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Follower(db.Model):
    user_username = db.Column(db.String(255), db.ForeignKey('user.username'), primary_key=True)
    follower_username = db.Column(db.String(255), db.ForeignKey('user.username'), primary_key=True)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_username = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    coordinates = db.Column(Geometry('POINT'))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    image = db.Column(db.String(255))
    time_created = db.Column(db.DateTime, default=db.func.current_timestamp())

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_username = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    experience_id = db.Column(db.Integer, db.ForeignKey('experience.id'), nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    experience_id = db.Column(db.Integer, db.ForeignKey('experience.id'), nullable=False)
    rating = db.Column(db.Float)

