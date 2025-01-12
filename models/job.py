from db import db
from datetime import datetime


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    commander_id = db.Column(db.Integer, db.ForeignKey('commanders.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    vacant_positions = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    education_requirement = db.Column(db.String(100))
    required_certificates = db.Column(db.String(200))
    required_languages = db.Column(db.String(200))
    hourly_salary = db.Column(db.Float)
    weekly_salary_cap = db.Column(db.Float)

    # Relationships
    questions = db.relationship('JobQuestion', backref='job', lazy=True)
    applications = db.relationship('JobApplication', backref='job', lazy=True)


class JobQuestion(db.Model):
    __tablename__ = 'job_questions'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    required = db.Column(db.Boolean, default=True)