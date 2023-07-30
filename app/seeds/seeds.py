# seed.py
import bcrypt
from ..app_instance import app, db
from ..models.models import User, Follower, Experience, Trip, Rating, TripExperience
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

    experience4 = Experience(
        user_username=user3.username,
        title="Great Wall of China",
        description="A giant wall!",
        coordinates=WKTElement(f'POINT({40.68} {117.23})', srid=4326),
        state="Hebei",
        country="China",
        image="https://osucapstone.blob.core.windows.net/images/Great-Wall-of-China-1-962246090.jpg",
    )

    experience5 = Experience(
        user_username=user3.username,
        title="National Museum of Nuclear Science & History",
        description="My geiger counter is off the charts!",
        coordinates=WKTElement(f'POINT({35.065985} {-106.533892})', srid=4326),
        state="New Mexico",
        country="United States",
        image="https://osucapstone.blob.core.windows.net/images/L37A1375-2579585453.jpg",
    )

    experience6 = Experience(
        user_username=user3.username,
        title="Sandia Peak Tramway",
        description="its a box, on a cable... on a mountain..",
        coordinates=WKTElement(f'POINT({35.1877} {-106.4743})', srid=4326),
        state="New Mexico",
        country="United States",
        image="https://osucapstone.blob.core.windows.net/images/L37A1375-2579585453.jpg",
    )

    db.session.add(experience1)
    db.session.add(experience2)
    db.session.add(experience3)
    db.session.add(experience4)

    #needed to add these to get some nearby experiences!
    db.session.add(experience5)
    db.session.add(experience6)

    db.session.commit()

    # Create test trips
    trip1 = Trip(
        trip_name="Summer Trip",
        user_username=user1.username
    )
    trip2 = Trip(
        trip_name="Winter Trip",
        user_username=user2.username
    )

    trip3 = Trip(
        trip_name="Autumn Trip",
        user_username=user1.username
    )

    db.session.add(trip1)
    db.session.add(trip2)
    db.session.add(trip3)

    db.session.commit()

    # Add experiences to the test trips
    trip1_experience_1 = TripExperience(
        trip_id=trip1.id,
        experience_id=experience1.id
    )

    trip1_experience_2 = TripExperience(
        trip_id=trip1.id,
        experience_id=experience2.id
    )

    trip2_experience_2 = TripExperience(
        trip_id=trip2.id,
        experience_id=experience2.id
    )
    db.session.add(trip1_experience_1)
    db.session.add(trip1_experience_2)
    db.session.add(trip2_experience_2)

    db.session.commit()

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
        rating=5.0
    )
    rating4 = Rating(
        username=user3.username,
        experience_id=experience2.id,
        rating=4.5
    )
    rating5 = Rating(
        username=user2.username,
        experience_id=experience3.id,
        rating=4.4
    )

    db.session.add(rating1)
    db.session.add(rating2)
    db.session.add(rating3)
    db.session.add(rating4)
    db.session.add(rating5)

    db.session.commit()
