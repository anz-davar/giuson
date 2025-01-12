from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     token, role = AuthService.login(data['email'], data['password'])
#
#     if token:
#         return jsonify({
#             'access_token': token,
#             'role': role
#         }), 200
#     return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        email = data['email']
        password = data['password']
        role = data['role']
        user_data = {k: v for k, v in data.items() if k not in ['email', 'password', 'role']}
        user, error = AuthService.create_user(email, password, role, **user_data)

        if error:
            return jsonify({"message": f"Error creating user: {error}"}), 400

        return jsonify({"message": "User created successfully"}), 201
    except KeyError as e:
        return jsonify({"message": f"Missing field: {e}"}), 400
    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {str(e)}"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    token, role = AuthService.login(email, password)

    if token:
        return jsonify({
            'access_token': token,
            'role': role
        }), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
