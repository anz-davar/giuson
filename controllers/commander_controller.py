from datetime import date
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.commander_service import CommanderService
from models.user import User
import io

commander_bp = Blueprint('commander', __name__)


@commander_bp.route('/jobs', methods=['POST'])
@jwt_required()
def create_job():
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'commander':
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    job = CommanderService.create_job(current_user.commander.id, data)

    return jsonify({
        'message': 'Job created successfully',
        'job_id': job.id
    }), 201


@commander_bp.route('/jobs', methods=['GET'])
@jwt_required()
def get_jobs():
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'commander':
        return jsonify({'message': 'Unauthorized'}), 403

    jobs = CommanderService.get_commander_jobs(current_user.commander.id)
    payload = [{
        'id': str(job.id),
        'jobName': job.title,
        'jobCategory': job.category,
        'unit': job.unit,
        'address': job.address,
        'positions': job.vacant_positions,
        'openBase': job.is_open_base,
        'closedBase': not job.is_open_base,
        'jobDescription': job.description,
        'additionalInfo': job.additional_info,
        'commonQuestions': job.common_questions,
        'commonAnswers': job.common_answers,
        'education': job.education,
        'techSkills': job.tech_skills,
        'workExperience': job.experience,
        'passedCourses': job.passed_courses,
        'candidateCount': len(job.applications),
        'status': job.status.name,
        'department': job.commander.department if job.commander else None,  # Get department from job
        'commanderId': job.commander_id,
        'applications_count': len(job.applications)
    } for job in jobs]

    return jsonify(payload), 200


@commander_bp.route('/jobs/<int:job_id>', methods=['PATCH'])
@jwt_required()
def patch_job_route(job_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'commander':
        return jsonify({'message': 'Unauthorized'}), 403

    job = CommanderService.get_job_by_id(job_id)
    if not job:
        return jsonify({'message': 'Job not found'}), 404

    data = request.get_json()

    updated_job = CommanderService.patch_job(job, data)

    return jsonify({'message': 'Job updated successfully', 'job': {
        'id': str(updated_job.id),
        'jobName': updated_job.title,
        'jobCategory': updated_job.category,
        'unit': updated_job.unit,
        'address': updated_job.address,
        'positions': updated_job.vacant_positions,
        'openBase': updated_job.is_open_base,
        'closedBase': not updated_job.is_open_base,
        'jobDescription': updated_job.description,
        'additionalInfo': updated_job.additional_info,
        'commonQuestions': updated_job.common_questions,
        'commonAnswers': updated_job.common_answers,
        'education': updated_job.education,
        'techSkills': updated_job.tech_skills,
        'workExperience': updated_job.experience,
        'passedCourses': updated_job.passed_courses,
        'candidateCount': len(updated_job.applications),
        'status': updated_job.status.name,
        'department': updated_job.commander.department if updated_job.commander else None,  # Get department from job
        'commanderId': updated_job.commander_id,
        'applications_count': len(updated_job.applications)
    }}), 200


def calculate_age(born):
    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError:
        birthday = born.replace(year=today.year, day=born.day - 1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year


@commander_bp.route('/jobs/<int:job_id>/applications', methods=['GET'])
@jwt_required()
def get_job_applications(job_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'commander':
        return jsonify({'message': 'Unauthorized'}), 403

    applications = CommanderService.get_job_applications(job_id, current_user.commander.id)
    return jsonify([{
        'candidateUserId': app.volunteer.user_id,
        'name': app.volunteer.full_name,
        'age': calculate_age(app.volunteer.date_of_birth) if app.volunteer.date_of_birth else None,
        'status': app.status.value
    } for app in applications]), 200


@commander_bp.route('/volunteers/<int:volunteer_id>', methods=['GET'])
@jwt_required()
def get_volunteer(volunteer_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'commander':
        return jsonify({'message': 'Unauthorized'}), 403

    volunteer = CommanderService.get_volunteer_by_id(volunteer_id)
    payload = {
        'id': volunteer.id,
        'fullName': volunteer.full_name,
        'idNumber': volunteer.national_id,  # Assuming national_id is the same as idNumber
        'dateOfBirth': volunteer.date_of_birth.strftime('%Y-%m-%d') if volunteer.date_of_birth else None,
        # Format dateOfBirth
        'age': calculate_age(volunteer.date_of_birth) if volunteer.date_of_birth else None,
        # Function to calculate age (optional)
        'gender': volunteer.gender.value if volunteer.gender else None,  # Handle potential null values
        'profile': volunteer.profile,
        'phone': volunteer.user.phone,
        'email': volunteer.user.email,
        'address': volunteer.address,
        'experience': volunteer.experience,
        'education': volunteer.education,
        'courses': volunteer.courses,
        'languages': volunteer.languages,  # Function to extract languages (optional)
        'interests': volunteer.interests,
        'personalSummary': volunteer.personal_summary,
        'jobStatuses': {str(job_app.job_id): job_app.status.value
                        for job_app in volunteer.applications},  # Map job application status
        'imageUrl': volunteer.user.image_url if volunteer.user.image_url else None  # Handle potential null values
    }

    return jsonify(payload), 200


@commander_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
@jwt_required()
def update_application_status(application_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'commander':
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    application = CommanderService.update_application_status(
        application_id,
        current_user.commander.id,
        data['status']
    )
    return jsonify({'message': 'Status updated successfully'}), 200


@commander_bp.route('/applications/<int:application_id>/interview', methods=['POST'])
@jwt_required()
def schedule_interview(application_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'commander':
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    interview = CommanderService.schedule_interview(
        application_id,
        current_user.commander.id,
        data
    )
    return jsonify({
        'message': 'Interview scheduled successfully',
        'interview_id': interview.id
    }), 201


@commander_bp.route('/jobs/<int:job_id>/applications/export', methods=['GET'])
@jwt_required()
def export_applications(job_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'commander':
        return jsonify({'message': 'Unauthorized'}), 403

    csv_data = CommanderService.generate_applications_csv(job_id, current_user.commander.id)
    if not csv_data:
        return jsonify({'message': 'No applications found'}), 404

    output = io.StringIO(csv_data)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'applications_job_{job_id}.csv'
    )
