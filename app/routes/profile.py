from flask import render_template
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import func
from app import app, db, container_client
from app.models.models import Experience, Follower, Rating, User
import json

@app.route('/profile', methods=["GET"])
@jwt_required()
def profile():
    username = get_jwt_identity()

    following = db.session.execute(db.Select(Follower).where(Follower.user_username == username)).scalars().all()
    followers = db.session.execute(db.Select(Follower).where(Follower.follower_username == username)).scalars().all()

    experiences = db.session.execute(db.Select(Experience).where(Experience.user_username == username)).scalars().all()


    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    user.time_created = user.time_created.strftime('%B %Y')

    

    return render_template('profile.html', user=user,
                            following_count=len(following),
                            followers_count=len(followers),
                            experiences=experiences,
                            experiences_count=len(experiences))