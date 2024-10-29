# models.py
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Developer(db.Model):
    __tablename__ = 'developers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    branch = db.Column(db.String, nullable=False)
    domain_mail_id = db.Column(db.String, nullable=False)
    domain_expertise = db.Column(db.String, nullable=False)
    projects = db.Column(db.Text, nullable=False)  # Change to Text for larger strings

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'branch': self.branch,
            'domain_mail_id': self.domain_mail_id,
            'domain_expertise': self.domain_expertise,
            'projects': json.loads(self.projects)  # Convert the string back to list
        }

    @property
    def projects_list(self):
        return json.loads(self.projects)  # Convert stored string back to list

    @projects_list.setter
    def projects_list(self, value):
        self.projects = json.dumps(value)  # Convert list to string for storage
