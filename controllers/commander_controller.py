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
        'department':job.commander.department if job.commander else None,   # Get department from job
        'commanderId': job.commander_id,
        'applications_count': len(job.applications)
    } for job in jobs]

    return jsonify(payload), 200
    # return jsonify([{
    #     'id': job.id,
    #     'title': job.title,
    #     'description': job.description,
    #     'vacant_positions': job.vacant_positions,
    #     'applications_count': len(job.applications)
    # } for job in jobs]), 200


@commander_bp.route('/jobs/<int:job_id>/applications', methods=['GET'])
@jwt_required()
def get_job_applications(job_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'commander':
        return jsonify({'message': 'Unauthorized'}), 403

    applications = CommanderService.get_job_applications(job_id, current_user.commander.id)
    return jsonify([{
        'candidateUserId': app.volunteer.user_id,
        'status': app.status.value
    } for app in applications]), 200


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