# seed.py
from ..app_instance import app, db
from ..models.models import User, Follower, Experience, Trip

def seed_data():
    db.drop_all()
    db.create_all()

    # Create test users
    user1 = User(
        firstname="TestUser1",
        lastname="User1",
        password="password"
    )
    user2 = User(
        firstname="TestUser2",
        lastname="User2",
        password="password"
    )
    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()

    # Make user1 follow user2
    follower_relation = Follower(
        user_id=user1.id,
        follower_id=user2.id
    )
    db.session.add(follower_relation)

    db.session.commit()

    # Create test experiences
    experience1 = Experience(
        user_id=user1.id,
        title="Kennedy Space Center",
        description="Its out of this world!",
        latitude=28.5729,
        longitude=80.6490,
        state="Florida",
        country="United States",
        image="image1.jpg",
        rating=4.5
    )
    experience2 = Experience(
        user_id=user2.id,
        title="Balloon Fiesta",
        description="Balloon Fiesta in Albuquerque NM!",
        latitude=35.0844,
        longitude=106.6504,
        state="New Mexico",
        country="United States",
        image="image2.jpg",
        rating=3.8
    )
    db.session.add(experience1)
    db.session.add(experience2)

    db.session.commit()

    # Create test trips
    trip1 = Trip(
        user_id=user1.id,
        experience_id=experience1.id
    )
    trip2 = Trip(
        user_id=user2.id,
        experience_id=experience2.id
    )
    db.session.add(trip1)
    db.session.add(trip2)

    db.session.commit()
