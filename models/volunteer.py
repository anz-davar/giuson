from db import db
from datetime import datetime


class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    national_id = db.Column(db.String(20), unique=True, nullable=False)
    age = db.Column(db.Integer)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    primary_profession = db.Column(db.String(100))
    education = db.Column(db.String(100))
    area_of_interest = db.Column(db.String(100))
    contact_reference = db.Column(db.String(200))

    # Relationships
    applications = db.relationship('JobApplication', backref='volunteer', lazy=True)
    resume = db.relationship('Resume', backref='volunteer', uselist=False)


class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteers.id'), nullable=False)
    file_path = db.Column(db.String(255))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
