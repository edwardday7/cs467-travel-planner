from flask import render_template, jsonify
from app import app, db
from app.models.models import User

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/users')
def users():
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    return render_template('users.html', users=users)

@app.route("/login", methods=["GET"])
def login():
    # username = request.json.get("username", None)
    # password = request.json.get("password", None)
    # if username != "test" or password != "test":
    #     return jsonify({"msg": "Bad username or password"}), 401

    # access_token = create_access_token(identity=username)
    # return jsonify(access_token=access_token)
    return render_template('login.html')

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200
