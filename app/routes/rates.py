from flask import make_response, redirect, render_template, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, db
from app.models.models import Rating


@app.route('/rate/experience/<experience_id>', methods=["GET", "POST"])
@jwt_required()
def rate_experience(experience_id):
    if request.method == "GET":
        current_user = get_jwt_identity(),
        # print("rate_experience if:", current_user)
        # print("rate_experience if:", experience_id)
        return render_template('rate_experience.html', current_user=current_user[0], experience_id=experience_id)
    else:
        # print("rate_experience else:")
        # print(request.form.get('username'))
        # print(request.form.get('experience_id'))
        # print(request.form.get('rating'))
        username = get_jwt_identity()

        print(username)
        print(experience_id)
        print(request.form.get('rating'))

        rating = Rating(
            username=username,
            experience_id=int(experience_id),
            rating=int(request.form.get('rating')),
        )

        print(rating)

        db.session.add(rating)
        db.session.commit()

        return redirect('/')
