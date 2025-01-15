# services/hr_service.py
from models import User, HR, Volunteer, JobApplication, Job
from services.auth_service import AuthService
from db import db
from flask import abort


class HRService:
    @staticmethod
    def create_hr_user(data):
        try:
            # Create base user with HR role
            user = AuthService.create_user(
                email=data['email'],
                password=data['password'],
                role='hr'
            )
            db.session.add(user)

            # Create HR profile
            hr = HR(
                user=user,
                name=data['name'],
                department=data.get('department'),
                phone=data.get('phone')
            )
            db.session.add(hr)
            db.session.commit()
            return hr
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def create_volunteer(data):
        try:
            # Create base user with volunteer role
            user = AuthService.create_user(
                email=data['email'],
                password=data['password'],
                role='volunteer'
            )
            db.session.add(user)

            # Create volunteer profile
            volunteer = Volunteer(
                user=user,
                full_name=data['full_name'],
                national_id=data['national_id'],
                age=data.get('age'),
                address=data.get('address'),
                phone=data.get('phone'),
                primary_profession=data.get('primary_profession'),
                education=data.get('education'),
                area_of_interest=data.get('area_of_interest'),
                contact_reference=data.get('contact_reference')
            )
            db.session.add(volunteer)
            db.session.commit()
            return volunteer
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_volunteers():
        return Volunteer.query.all()

    @staticmethod
    def get_volunteer_by_id(volunteer_id):
        return Volunteer.query.get_or_404(volunteer_id)

    @staticmethod
    def get_all_jobs():
        return Job.query.all()

    @staticmethod
    def assign_volunteer_to_job(volunteer_id, job_id):
        try:
            # Check if volunteer and job exist
            volunteer = Volunteer.query.get_or_404(volunteer_id)
            job = Job.query.get_or_404(job_id)

            # Check if there's an existing application
            application = JobApplication.query.filter_by(
                volunteer_id=volunteer_id,
                job_id=job_id
            ).first()

            if not application:
                abort(404, description="No application found for this volunteer and job")

            if application.status != 'accepted':
                abort(400, description="Application must be accepted by commander first")

            if job.vacant_positions <= 0:
                abort(400, description="No vacant positions available")

            # Update job vacancy
            job.vacant_positions -= 1

            # Update application status to assigned
            application.status = 'assigned'

            db.session.commit()
            return application
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_volunteer_applications(volunteer_id):
        return JobApplication.query.filter_by(volunteer_id=volunteer_id).all()

    @staticmethod
    def get_job_applications(job_id):
        return JobApplication.query.filter_by(job_id=job_id).all()

    @staticmethod
    def update_volunteer(volunteer_id, data):
        try:
            volunteer = Volunteer.query.get_or_404(volunteer_id)

            # Update volunteer fields
            for key, value in data.items():
                if hasattr(volunteer, key):
                    setattr(volunteer, key, value)

            db.session.commit()
            return volunteer
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_hr_user_info(user_id):
        return User.query.filter_by(id=user_id).first()
