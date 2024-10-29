from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Developer

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Enable CORS for specific origins
CORS(app, origins=["http://localhost:5173", "http://seshasai.tech"])

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
        # Check if developer already exists before adding
        if not Developer.query.filter_by(name=dev['name']).first():
            new_developer = Developer(
                name=dev['name'],
                branch=dev['branch'],
                domain_mail_id=dev['domain_mail_id'],
                domain_expertise=dev['domain_expertise'],
                projects=dev['projects']
            )
            db.session.add(new_developer)

    db.session.commit()

with app.app_context():
    db.create_all()  # Create the database tables
    add_default_developers()  # Add default developers

@app.route('/api/developers', methods=['GET'])
def get_developers():
    name = request.args.get('name', '').strip()
    domain = request.args.get('domain', '').strip()

    query = Developer.query

    if name:
        query = query.filter(Developer.name.ilike(f'%{name}%'))

    if domain:
        query = query.filter(Developer.domain_expertise.ilike(f'%{domain}%'))

    developers = query.all()
    return jsonify([developer.to_dict() for developer in developers])

@app.route('/api/developers', methods=['POST'])
def add_developer():
    data = request.json
    new_developer = Developer(
        name=data['name'],
        branch=data['branch'],
        domain_mail_id=data['domain_mail_id'],
        domain_expertise=data['domain_expertise'],
        projects=data['projects']
    )
    db.session.add(new_developer)
    db.session.commit()
    return jsonify(new_developer.to_dict()), 201

@app.route('/api/developers/<int:id>', methods=['GET'])
def get_developer(id):
    developer = Developer.query.get_or_404(id)
    return jsonify(developer.to_dict())

@app.route('/api/developers/<int:id>', methods=['PUT'])
def update_developer(id):
    data = request.json
    developer = Developer.query.get_or_404(id)

    developer.name = data['name']
    developer.branch = data['branch']
    developer.domain_mail_id = data['domain_mail_id']
    developer.domain_expertise = data['domain_expertise']
    developer.projects = data['projects']

    db.session.commit()
    return jsonify(developer.to_dict())

@app.route('/api/developers/<int:id>', methods=['DELETE'])
def delete_developer(id):
    developer = Developer.query.get_or_404(id)
    db.session.delete(developer)
    db.session.commit()
    return jsonify({"message": "Developer deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
