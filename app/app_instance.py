# app_instance.py
import datetime
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = os.environ.get("AUTH_SECRET") or "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=12)
app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
db = SQLAlchemy(app)
