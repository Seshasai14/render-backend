# flask_api/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Developer(db.Model):
    __tablename__ = 'developers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    domain_mail_id = db.Column(db.String(100), unique=True, nullable=False)
    domain_expertise = db.Column(db.String(100), nullable=False)
    projects = db.Column(db.Text, nullable=True)  # Store as comma-separated values or JSON

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'branch': self.branch,
            'domain_mail_id': self.domain_mail_id,
            'domain_expertise': self.domain_expertise,
            'projects': self.projects.split(',') if self.projects else [],  # Convert string to list
        }
