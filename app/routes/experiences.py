from flask import make_response, redirect, render_template, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, db
from app.models.models import Experience

@app.route('/experiences/new', methods=["GET", "POST"])
@jwt_required()
def create_experience():
    if request.method == "GET":
        return render_template('create_experience.html')
    else:
        new_experience = Experience(
            user_username=get_jwt_identity(),
            title=request.form.get('title'),
            description=request.form.get('description'),
            latitude=float(request.form.get('latitude')),
            longitude=float(request.form.get('longitude')),
            state=request.form.get('state'),
            country=request.form.get('country'),
            image="image3.jpg" # TODO image upload
        )

        print(new_experience)
        
        db.session.add(new_experience)
        db.session.commit()

        return redirect('/')