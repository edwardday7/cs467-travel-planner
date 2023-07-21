# __init__.py
from .app_instance import app, db, jwt, container_client
from .seeds.seeds import seed_data

from .models.models import User

with app.app_context():
    # Seed some test data
    seed_data()

from .routes import auth, routes, experiences, rates

