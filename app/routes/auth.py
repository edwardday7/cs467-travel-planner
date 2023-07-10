import bcrypt
from flask import render_template, request, make_response, redirect
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from app import app, db
from app.models.models import User
from ..app_instance import jwt

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template('login.html'), 401

        user = db.session.execute(db.select(User).where(User.username == username)).scalar()
        
        if not user:
            return render_template('login.html'), 401

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return render_template('login.html'), 401

        access_token = create_access_token(identity=user.username)

        response = make_response(redirect('/', 302))
        set_access_cookies(response, encoded_access_token=access_token)
        return response
    
@app.route("/logout", methods=["GET", "POST"])
def logout():
    response = make_response(redirect('/login'))
    unset_jwt_cookies(response)
    return response

@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return redirect('/login', 302)

@jwt.unauthorized_loader
def unauthorized(error_message):
    return redirect('/login', 302)

def create_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')