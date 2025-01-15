from datetime import datetime

from werkzeug.exceptions import BadRequest

from models import JobApplication, ApplicationAnswer, Resume, User
from db import db
import os

from models.volunteer import Volunteer


class VolunteerService:

    @staticmethod
    def apply_for_job(volunteer_id, job_id, data):
        existing_application = JobApplication.query.filter_by(
            volunteer_id=volunteer_id, job_id=job_id).first()
        if existing_application:
            raise BadRequest("You have already applied for this job")

        application = JobApplication(
            volunteer_id=volunteer_id,
            job_id=job_id,
            **data  # Unpack data dictionary into keyword arguments
        )
        db.session.add(application)
        db.session.commit()
        return application

    # @staticmethod
    # def apply_for_job(volunteer_id, job_id, data):
    #     application = JobApplication(
    #         volunteer_id=volunteer_id,
    #         job_id=job_id
    #     )
    #     db.session.add(application)

        # # Add answers
        # for answer in data.get('answers', []):
        #     app_answer = ApplicationAnswer(
        #         application=application,
        #         question_id=answer['question_id'],
        #         answer_text=answer['text']
        #     )
        #     db.session.add(app_answer)

        # db.session.commit()
        # return application

    @staticmethod
    def delete_application(volunteer_id, job_id):
        application = JobApplication.query.filter_by(
            volunteer_id=volunteer_id, job_id=job_id).first()
        if not application:
            return None

        db.session.delete(application)
        db.session.commit()
        return application
    @staticmethod
    def upload_resume(volunteer_id, file):
        # Handle file upload logic here
        filename = f"resume_{volunteer_id}_{file.filename}"
        file_path = os.path.join('uploads', 'resumes', filename)

        resume = Resume(
            volunteer_id=volunteer_id,
            file_path=file_path
        )
        db.session.add(resume)
        db.session.commit()

        # Save file
        file.save(file_path)
        return resume
    
    @staticmethod
    def get_user_info(user_id):
        return Volunteer.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_volunteer_by_user_id(user_id):
        user = User.query.get(user_id)
        if not user or not user.volunteer:
            return None
        return user.volunteer

    @staticmethod
    def update_volunteer_details_by_user_id(user_id, data):
        volunteer = VolunteerService.get_volunteer_by_user_id(user_id)
        if not volunteer:
            raise BadRequest("Volunteer not found")

        user = volunteer.user

        volunteer_data = {}
        user_data = {}

        if 'date_of_birth' in data:
            try:
                date_str = data['date_of_birth']
                date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ').date()
                data['date_of_birth'] = date_obj
            except ValueError:
                raise BadRequest(
                    "Invalid date format for date_of_birth. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sssZ).")

        for key, value in data.items():
            if hasattr(volunteer, key):
                volunteer_data[key] = value
            elif hasattr(user, key):
                user_data[key] = value
            else:
                raise BadRequest(f"Invalid field to update: {key}")

        # Update Volunteer fields
        for key, value in volunteer_data.items():
            setattr(volunteer, key, value)

        # Update User fields
        for key, value in user_data.items():
            setattr(user, key, value)

        db.session.commit()
        return volunteer
