import enum

from db import db
from datetime import datetime


class ApplicationStatus(enum.Enum):
    PENDING = "pending"
    PREFERRED = "preferred"
    REJECTED = "rejected"
    HIRED = "hired"
    def __str__(self):
        return self.value


class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteers.id'), nullable=False)
    status = db.Column(db.Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    # resume = db.relationship('Resume', uselist=False, backref='application')
    resume = db.relationship('Resume', back_populates='application', cascade="all, delete-orphan", uselist=False)

    # Relationships
    answers = db.relationship('ApplicationAnswer', backref='application', lazy=True)
    interview = db.relationship('Interview', backref='application', cascade="all, delete-orphan", uselist=False)



class ApplicationAnswer(db.Model):
    __tablename__ = 'application_answers'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('job_applications.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('job_questions.id'), nullable=False)
    answer_text = db.Column(db.Text)
