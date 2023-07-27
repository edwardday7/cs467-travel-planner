import uuid
from flask import make_response, redirect, render_template, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import app, db, container_client
from app.models.models import Experience
from sqlalchemy import desc, or_

@app.route('/experiences', methods=['GET'])
def experiences():
    search = request.args.get('q')
    sort = request.args.get('sort')
    
    if search:
        experiences = Experience.query.filter(or_(Experience.title.contains(search), Experience.description.contains(search)))
    else:
        experiences = Experience.query

    #this is borked
    if sort == 'highest_rating':
        experiences = experiences.order_by(Experience.rating.desc())
    elif sort == 'lowest_rating':
        experiences = experiences.order_by(Experience.rating.asc())

    experiences = experiences.all()

    return render_template('experiences.html', experiences=experiences)

@app.route('/experience/<int:experience_id>', methods=['GET'])
def experience_detail(experience_id):
    experience = Experience.query.get_or_404(experience_id)
    return render_template('experience_detail.html', experience=experience)

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
            image=upload_file(request.files.get('file')).url  # blob_client.url
        )
        
        db.session.add(new_experience)
        db.session.commit()

        return redirect('/')
    
def upload_file(image):
    return container_client.upload_blob(image.filename + str(uuid.uuid4()), image)