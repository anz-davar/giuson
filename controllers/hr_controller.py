# controllers/hr_controller.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.hr_service import HRService
from models import User

hr_bp = Blueprint('hr', __name__)


@hr_bp.route('/hr', methods=['POST'])
def create_hr():
    """Create a new HR user"""
    try:
        data = request.get_json()
        hr = HRService.create_hr_user(data)
        return jsonify({
            'message': 'HR user created successfully',
            'hr_id': hr.id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@hr_bp.route('/volunteers', methods=['POST'])
@jwt_required()
def create_volunteer():
    """Create a new volunteer user"""
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'hr':
        return jsonify({'message': 'Unauthorized'}), 403

    try:
        data = request.get_json()
        volunteer = HRService.create_volunteer(data)
        return jsonify({
            'message': 'Volunteer created successfully',
            'volunteer_id': volunteer.id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@hr_bp.route('/volunteers', methods=['GET'])
@jwt_required()
def get_volunteers():
    """Get all volunteers"""
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'hr':
        return jsonify({'message': 'Unauthorized'}), 403

    volunteers = HRService.get_all_volunteers()
    return jsonify([{
        'id': v.id,
        'full_name': v.full_name,
        'email': v.user.email,
        'phone': v.phone,
        'education': v.education,
        'primary_profession': v.primary_profession
    } for v in volunteers]), 200


@hr_bp.route('/volunteers/<int:volunteer_id>', methods=['GET'])
@jwt_required()
def get_volunteer(volunteer_id):
    """Get specific volunteer details"""
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'hr':
        return jsonify({'message': 'Unauthorized'}), 403

    volunteer = HRService.get_volunteer_by_id(volunteer_id)
    return jsonify({
        'id': volunteer.id,
        'full_name': volunteer.full_name,
        'email': volunteer.user.email,
        'phone': volunteer.phone,
        'education': volunteer.education,
        'primary_profession': volunteer.primary_profession,
        'area_of_interest': volunteer.area_of_interest
    }), 200


@hr_bp.route('/jobs', methods=['GET'])
@jwt_required()
def get_jobs():
    """Get all jobs"""
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'hr':
        return jsonify({'message': 'Unauthorized'}), 403

    jobs = HRService.get_all_jobs()
    return jsonify([{
        'id': job.id,
        'title': job.title,
        'commander_name': job.commander.name,
        'vacant_positions': job.vacant_positions,
        'applications_count': len(job.applications)
    } for job in jobs]), 200


@hr_bp.route('/assignments', methods=['POST'])
@jwt_required()
def assign_volunteer():
    """Assign a volunteer to a job"""
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'hr':
        return jsonify({'message': 'Unauthorized'}), 403

    try:
        data = request.get_json()
        application = HRService.assign_volunteer_to_job(
            data['volunteer_id'],
            data['job_id']
        )
        return jsonify({
            'message': 'Volunteer assigned successfully',
            'application_id': application.id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@hr_bp.route('/volunteers/<int:volunteer_id>/applications', methods=['GET'])
@jwt_required()
def get_volunteer_applications(volunteer_id):
    """Get all applications for a specific volunteer"""
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'hr':
        return jsonify({'message': 'Unauthorized'}), 403

    applications = HRService.get_volunteer_applications(volunteer_id)
    return jsonify([{
        'id': app.id,
        'job_title': app.job.title,
        'status': app.status,
        'application_date': app.application_date.isoformat()
    } for app in applications]), 200


@hr_bp.route('/jobs/<int:job_id>/applications', methods=['GET'])
@jwt_required()
def get_job_applications(job_id):
    """Get all applications for a specific job"""
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'hr':
        return jsonify({'message': 'Unauthorized'}), 403

    applications = HRService.get_job_applications(job_id)
    return jsonify([{
        'id': app.id,
        'volunteer_name': app.volunteer.full_name,
        'status': app.status,
        'application_date': app.application_date.isoformat()
    } for app in applications]), 200


@hr_bp.route('/volunteers/<int:volunteer_id>', methods=['PUT'])
@jwt_required()
def update_volunteer(volunteer_id):
    """Update volunteer information"""
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'hr':
        return jsonify({'message': 'Unauthorized'}), 403

    try:
        data = request.get_json()
        volunteer = HRService.update_volunteer(volunteer_id, data)
        return jsonify({
            'message': 'Volunteer updated successfully',
            'volunteer_id': volunteer.id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
