from flask import render_template, jsonify
from app import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200
