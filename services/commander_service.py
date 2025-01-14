from models.commander import Commander
from models.job import Job, JobQuestion, JobStatus
from models.interview import Interview
from models.application import JobApplication
from db import db
from datetime import datetime
from flask import abort
import csv
import io
from werkzeug.exceptions import BadRequest


class CommanderService:
    @staticmethod
    def create_commander(user_id, data):
        commander = Commander(
            user_id=user_id,
            name=data['name'],
            department=data.get('department'),
            rank=data.get('rank'),
            phone=data.get('phone')
        )
        db.session.add(commander)
        db.session.commit()
        return commander

    @staticmethod
    def create_job(commander_id, data):
        # job = Job(
        #     commander_id=commander_id,
        #     title=data['title'],
        #     description=data['description'],
        #     vacant_positions=data.get('vacant_positions', 1),
        #     education_requirement=data.get('education_requirement'),
        #     required_certificates=data.get('required_certificates'),
        #     required_languages=data.get('required_languages'),
        #     hourly_salary=data.get('hourly_salary'),
        #     weekly_salary_cap=data.get('weekly_salary_cap')
        # )
        job = Job(
            commander_id=commander_id,
            title=data['name'],  # Map name to title
            description=data['description'],
            vacant_positions=data.get('positions', 1),
            category=data.get('category'),
            unit=data.get('unit'),
            address=data.get('address'),
            is_open_base=data.get('openBase', True),
            additional_info=data.get('additionalInfo'),
            common_questions=data.get('questions'),
            common_answers=data.get('answers'),
            experience=data.get('workExperience'),
            education=data.get('education'),
            passed_courses=data.get('passedCourses'),
            tech_skills=data.get('techSkills'),
        )

        db.session.add(job)

        # Add questions TODO maybe return later multiple qustions and answers
        # for question_data in data.get('questions', []):
        #     question = JobQuestion(
        #         job=job,
        #         question_text=question_data['text'],
        #         required=question_data.get('required', True)
        #     )
        #     db.session.add(question)

        db.session.commit()
        return job

    @staticmethod
    def get_commander_jobs(commander_id):
        return Job.query.filter_by(commander_id=commander_id).all()

    @staticmethod
    def get_job_by_id(job_id):
        return Job.query.get(job_id)

    @staticmethod
    def patch_job(job, data):
        data = {k.lower(): v for k, v in data.items()}

        field_mapping = {
            'name': 'title',
            'description': 'description',
            'positions': 'vacant_positions',
            'category': 'category',
            'unit': 'unit',
            'address': 'address',
            'openbase': 'is_open_base',
            'additionalinfo': 'additional_info',
            'questions': 'common_questions',
            'answers': 'common_answers',
            'workexperience': 'experience',
            'education': 'education',
            'passedcourses': 'passed_courses',
            'techskills': 'tech_skills',
            'status': 'status'
        }
        print(data)
        for frontend_key, model_field in field_mapping.items():
            if frontend_key in data:
                print(frontend_key, model_field)
                value = data[frontend_key]

                if model_field == 'status':
                    try:
                        value = JobStatus(value)
                    except ValueError:
                        raise BadRequest(f"Invalid status value: {value}")
                setattr(job, model_field, value)

        db.session.commit()
        return job

    @staticmethod
    def get_job_applications(job_id, commander_id):
        job = Job.query.filter_by(id=job_id, commander_id=commander_id).first()
        if not job:
            abort(404)
        return JobApplication.query.filter_by(job_id=job_id).all()

    @staticmethod
    def update_application_status(application_id, commander_id, status):
        application = JobApplication.query.get_or_404(application_id)
        if application.job.commander_id != commander_id:
            abort(403)
        application.status = status
        db.session.commit()
        return application

    @staticmethod
    def schedule_interview(application_id, commander_id, interview_data):
        application = JobApplication.query.get_or_404(application_id)
        if application.job.commander_id != commander_id:
            abort(403)

        interview = Interview(
            application_id=application_id,
            scheduled_date=datetime.fromisoformat(interview_data['scheduled_date']),
            schedule=interview_data.get('schedule'),
            status='scheduled'
        )
        db.session.add(interview)
        application.status = 'interview_scheduled'
        db.session.commit()
        return interview

    @staticmethod
    def update_interview_results(interview_id, commander_id, results_data):
        interview = Interview.query.get_or_404(interview_id)
        if interview.application.job.commander_id != commander_id:
            abort(403)

        interview.management_results = results_data.get('management_results')
        interview.personal_results = results_data.get('personal_results')
        interview.summary = results_data.get('summary')
        interview.status = 'completed'
        db.session.commit()
        return interview

    @staticmethod
    def generate_applications_csv(job_id, commander_id):
        applications = JobApplication.query.filter_by(job_id=job_id).all()
        if not applications:
            return None

        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(['Application ID', 'Volunteer Name', 'Status', 'Application Date',
                         'Phone', 'Email', 'Education', 'Interview Status'])

        # Write data
        for app in applications:
            writer.writerow([
                app.id,
                app.volunteer.full_name,
                app.status,
                app.application_date.strftime('%Y-%m-%d'),
                app.volunteer.phone,
                app.volunteer.user.email,
                app.volunteer.education,
                app.interview.status if app.interview else 'No interview'
            ])

        return output.getvalue()
