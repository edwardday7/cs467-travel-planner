from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
db = SQLAlchemy()

db.init_app(app)

from app.models.models import User

with app.app_context():
    db.drop_all()
    db.create_all()

    # Seed some test data
    newUser = User(id=None, name="Test user")
    db.session.add(newUser)
    db.session.commit()

from app.routes import routes