# seed.py
import bcrypt
from ..app_instance import app, db
from ..models.models import User, Follower, Experience, Trip, Rating
from ..routes.auth import create_password
from geoalchemy2 import WKTElement

def seed_data():
    db.drop_all()
    db.create_all()

    # Create test users
    user1 = User(
        username="TestUser1",
        password=create_password("password")
    )
    user2 = User(
        username="TestUser2",
        password=create_password("password2"),
    )

    user3 = User(
        username="TestUser3",
        password=create_password("password3"),
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    db.session.commit()

    # Make user1 follow user2
    follower_relation = Follower(
        user_username=user1.username,
        follower_username=user2.username
    )

    follower_relation2 = Follower(
        user_username=user1.username,
        follower_username=user3.username
    )

    follower_relation3 = Follower(
        user_username=user2.username,
        follower_username=user3.username
    )

    follower_relation4 = Follower(
        user_username=user3.username,
        follower_username=user1.username
    )

    db.session.add(follower_relation)
    db.session.add(follower_relation2)
    db.session.add(follower_relation3)
    db.session.add(follower_relation4)

    db.session.commit()

    # Create test experiences
    experience1 = Experience(
        user_username=user1.username,
        title="Kennedy Space Center",
        description="Its out of this world!",
        coordinates=WKTElement(f'POINT({28.5729} {-80.6490})', srid=4326),
        state="Florida",
        country="United States",
        image="https://osucapstone.blob.core.windows.net/images/kennedy-space-center-florida_18000_xl-2795190506.jpg",
    )
    experience2 = Experience(
        user_username=user2.username,
        title="Balloon Fiesta",
        description="Balloon Fiesta in Albuquerque NM!",
        coordinates=WKTElement(f'POINT({35.0844} {-106.6504})', srid=4326),
        state="New Mexico",
        country="United States",
        image="https://osucapstone.blob.core.windows.net/images/L37A1375-2579585453.jpg",
    )

    experience3 = Experience(
        user_username=user3.username,
        title="Eiffel Tower",
        description="Tall and pointy!",
        coordinates=WKTElement(f'POINT({48.8584} {2.2945})', srid=4326),
        state="Ile-de-France",
        country="France",
        image="https://osucapstone.blob.core.windows.net/images/Eiffel-Tower-Paris-France-2-900045411.jpg",
    )

    db.session.add(experience1)
    db.session.add(experience2)
    db.session.add(experience3)

    db.session.commit()

    # Create test trips
    trip1 = Trip(
        user_username=user1.username,
        experience_id=experience1.id
    )
    trip2 = Trip(
        user_username=user2.username,
        experience_id=experience2.id
    )
    db.session.add(trip1)
    db.session.add(trip2)

    # Create test ratings
    rating1 = Rating(
        username=user2.username,
        experience_id=experience1.id,
        rating=4.5
    )
    rating2 = Rating(
        username=user3.username,
        experience_id=experience1.id,
        rating=3.8
    )
    rating3 = Rating(
        username=user1.username,
        experience_id=experience2.id,
        rating=4.0
    )
    rating4 = Rating(
        username=user3.username,
        experience_id=experience2.id,
        rating=4.5
    )
    rating5 = Rating(
        username=user2.username,
        experience_id=experience3.id,
        rating=5
    )

    db.session.add(rating1)
    db.session.add(rating2)
    db.session.add(rating3)
    db.session.add(rating4)
    db.session.add(rating5)

    db.session.commit()
