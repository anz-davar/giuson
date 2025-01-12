from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.volunteer_service import VolunteerService
from models import User, Job

volunteer_bp = Blueprint('volunteer', __name__)


@volunteer_bp.route('/jobs', methods=['GET'])
@jwt_required()
def get_available_jobs():
    jobs = Job.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': job.id,
        'title': job.title,
        'description': job.description,
        'vacant_positions': job.vacant_positions
    } for job in jobs]), 200


@volunteer_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
@jwt_required()
def apply_for_job(job_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'volunteer':
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    application = VolunteerService.apply_for_job(
        current_user.volunteer.id,
        job_id,
        data
    )
    return jsonify({'message': 'Application submitted successfully'}), 201