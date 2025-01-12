from models import JobApplication, ApplicationAnswer, Resume
from db import db
import os


class VolunteerService:
    @staticmethod
    def apply_for_job(volunteer_id, job_id, data):
        application = JobApplication(
            volunteer_id=volunteer_id,
            job_id=job_id
        )
        db.session.add(application)

        # Add answers
        for answer in data.get('answers', []):
            app_answer = ApplicationAnswer(
                application=application,
                question_id=answer['question_id'],
                answer_text=answer['text']
            )
            db.session.add(app_answer)

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