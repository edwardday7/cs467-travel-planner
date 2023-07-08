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

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200
