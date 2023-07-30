from app import db
from geoalchemy2 import Geometry
from sqlalchemy import func

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
    coordinates = db.Column(Geometry(geometry_type='POINT', srid=4326))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    image = db.Column(db.String(255))
    time_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    #used to get nearby experiences on experience details pages
    def get_nearby_experiences(self, distance_in_miles=50):
        distance_in_meters = distance_in_miles * 1609.34
        experiences = Experience.query.all()
        nearby_experiences = []
        for experience in experiences:
            if experience.id == self.id:
                continue
            distance = db.session.query(
                func.ST_Distance_Sphere(
                    self.coordinates, experience.coordinates
                )
            ).scalar()
            if distance <= distance_in_meters:
                nearby_experiences.append(experience)
        return nearby_experiences

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_name = db.Column(db.String(255))
    user_username = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)

class TripExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    experience_id = db.Column(db.Integer, db.ForeignKey('experience.id'), nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)
    experience_id = db.Column(db.Integer, db.ForeignKey('experience.id'), nullable=False)
    rating = db.Column(db.Float)

