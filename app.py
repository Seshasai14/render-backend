from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import CORS
from models import db, Developer

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Enable CORS for specific origins
CORS(app, origins=["http://localhost:5173", "http://seshasai.tech"])

with app.app_context():
    db.create_all()  # Create the database tables

@app.route('/api/developers', methods=['GET'])
def get_developers():
    name = request.args.get('name', '').strip()  # Get the name filter from the query parameters
    domain = request.args.get('domain', '').strip()  # Get the domain filter from the query parameters

    query = Developer.query  # Start with all developers

    # Filter by name if provided
    if name:
        query = query.filter(Developer.name.ilike(f'%{name}%'))  # Case-insensitive search

    # Filter by domain if provided
    if domain:
        query = query.filter(Developer.domain_expertise.ilike(f'%{domain}%'))  # Case-insensitive domain filtering

    developers = query.all()  # Execute the query
    return jsonify([developer.to_dict() for developer in developers])  # Return the filtered developers

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
