# seed.py
import bcrypt
from ..app_instance import app, db
from ..models.models import User, Follower, Experience, Trip
from ..routes.auth import create_password

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

    db.session.add(follower_relation)
    db.session.add(follower_relation2)

    db.session.commit()

    # Create test experiences
    experience1 = Experience(
        user_username=user1.username,
        title="Kennedy Space Center",
        description="Its out of this world!",
        latitude=28.5729,
        longitude=-80.6490,
        state="Florida",
        country="United States",
        image="image1.jpg",
        rating=4.5
    )
    experience2 = Experience(
        user_username=user2.username,
        title="Balloon Fiesta",
        description="Balloon Fiesta in Albuquerque NM!",
        latitude=35.0844,
        longitude=-106.6504,
        state="New Mexico",
        country="United States",
        image="image2.jpg",
        rating=3.8
    )

    experience3 = Experience(
        user_username=user3.username,
        title="Eiffel Tower",
        description="Tall and pointy!",
        latitude=48.8584,
        longitude=-106.6504,
        state="Ile-de-France",
        country="France",
        image="image3.jpg",
        rating=3.8
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

    db.session.commit()
