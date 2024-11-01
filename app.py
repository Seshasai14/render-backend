from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from models import db, Developer

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Enable CORS for specific origins
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Function to add default developers
def add_default_developers():
    default_developers = [
        {
            "name": "Archana",
            "branch": "Computer Science And Engineering",
            "domain_mail_id": "21131A05A1@sairam.ac.in",
            "domain_expertise": "Backend Development",
            "projects": ["Personal Blogging Platform API", "Expense Tracker API"]
        },
        {
            "name": "Swayam Krishna",
            "branch": "Mechanical Engineering",
            "domain_mail_id": "21131a03H7@gvpce.ac.in",
            "domain_expertise": "CAD",
            "projects": ["Motor Building", "Motor Repairing"]
        },
        {
            "name": "Sesha Sai",
            "branch": "Computer Science And Engineering",
            "domain_mail_id": "21131A05G1@gvpce.ac.in",
            "domain_expertise": "Frontend Development",
            "projects": ["Weather Application", "Chat Application"]
        },
        {
            "name": "Vivek Vardhan",
            "branch": "Computer Science And Engineering",
            "domain_mail_id": "21131A05H8@gvpce.ac.in",
            "domain_expertise": "Backend Development",
            "projects": ["Markdown Note-taking App", "URL Shortening Service"]
        },
        {
            "name": "Kusuma",
            "branch": "Computer Science And Engineering",
            "domain_mail_id": "21131A05H6@gvpce.ac.in",
            "domain_expertise": "Mobile Development",
            "projects": ["Blood Donation App", "Expense Tracker App"]
        },
        {
            "name": "Mounika",
            "branch": "Computer Science And Engineering",
            "domain_mail_id": "21131A05H3@gvpce.ac.in",
            "domain_expertise": "Mobile Developer",
            "projects": ["Calculator App", "Social Media App"]
        },
        {
            "name": "Arun",
            "branch": "Computer Science And Engineering",
            "domain_mail_id": "gnaneshkumargurrala@gmail.com",
            "domain_expertise": "Full Stack Development",
            "projects": ["Restaurant Site", "E Commerce Site"]
        }
    ]

    for dev in default_developers:
        if not Developer.query.filter_by(name=dev['name']).first():
            new_developer = Developer(
                name=dev['name'],
                branch=dev['branch'],
                domain_mail_id=dev['domain_mail_id'],
                domain_expertise=dev['domain_expertise'],
                projects=json.dumps(dev['projects'])  # Convert list to JSON string
            )
            db.session.add(new_developer)

    db.session.commit()

with app.app_context():
    db.create_all()  # Create the database tables
    add_default_developers()  # Add default developers

from sqlalchemy import or_
from flask import request, jsonify, make_response

@app.route('/api/developers', methods=['GET'])
def get_developers():
    search_term = request.args.get('searchTerm', '').strip()

    query = Developer.query

    if search_term:
        query = query.filter(
            or_(
                Developer.name.ilike(f'%{search_term}%'),
                Developer.domain_expertise.ilike(f'%{search_term}%'),
                Developer.branch.ilike(f'%{search_term}%'),
                Developer.projects.ilike(f'%{search_term}%')  
            )
        )

    developers = query.all()
    response = make_response(jsonify([developer.to_dict() for developer in developers]))
    response.headers["Access-Control-Allow-Origin"] = "http://seshasai.tech"  
    return response


@app.route('/api/developers', methods=['POST'])
def add_developer():
    data = request.json
    new_developer = Developer(
        name=data['name'],
        branch=data['branch'],
        domain_mail_id=data['domain_mail_id'],
        domain_expertise=data['domain_expertise'],
        projects=json.dumps(data['projects'])  # Convert list to JSON string
    )
    db.session.add(new_developer)
    db.session.commit()
    response = make_response(jsonify(new_developer.to_dict()), 201)
    response.headers["Access-Control-Allow-Origin"] = "http://seshasai.tech"
    return response

@app.route('/api/developers/<int:id>', methods=['GET'])
def get_developer(id):
    developer = Developer.query.get_or_404(id)
    response = make_response(jsonify(developer.to_dict()))
    response.headers["Access-Control-Allow-Origin"] = "http://seshasai.tech"
    return response

@app.route('/api/developers/<int:id>', methods=['PUT'])
def update_developer(id):
    data = request.json
    developer = Developer.query.get_or_404(id)

    developer.name = data['name']
    developer.branch = data['branch']
    developer.domain_mail_id = data['domain_mail_id']
    developer.domain_expertise = data['domain_expertise']
    developer.projects = json.dumps(data['projects'])  # Convert list to JSON string

    db.session.commit()
    response = make_response(jsonify(developer.to_dict()))
    response.headers["Access-Control-Allow-Origin"] = "http://seshasai.tech"
    return response

@app.route('/api/developers/<int:id>', methods=['DELETE'])
def delete_developer(id):
    developer = Developer.query.get_or_404(id)
    db.session.delete(developer)
    db.session.commit()
    response = make_response(jsonify({"message": "Developer deleted successfully!"}))
    response.headers["Access-Control-Allow-Origin"] = "http://seshasai.tech"
    return response
@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "https://seshasai.tech"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


if __name__ == '__main__':
    app.run(debug=True)
