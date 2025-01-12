from db import db
from datetime import datetime


class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteers.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, interview, accepted, rejected
    application_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    answers = db.relationship('ApplicationAnswer', backref='application', lazy=True)
    interview = db.relationship('Interview', backref='application', uselist=False)


class ApplicationAnswer(db.Model):
    __tablename__ = 'application_answers'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('job_applications.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('job_questions.id'), nullable=False)
    answer_text = db.Column(db.Text)