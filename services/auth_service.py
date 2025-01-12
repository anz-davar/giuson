from datetime import datetime

from flask_jwt_extended import create_access_token

from db import db
from models import *


class AuthService:
    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = AuthService.generate_token(user)
            return access_token, user.role
        return None, None

    # @staticmethod
    # def generate_token(user):
    #     payload = {
    #         'user_id': user.id,
    #         'role': user.role,
    #         'exp': datetime.utcnow() + timedelta(hours=24)
    #     }
    #     token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    #     return token

    @staticmethod
    def generate_token(user):
        # Create a token with user ID as the 'sub' claim
        token = create_access_token(
            identity=user.id,  # This sets the 'sub' claim
            additional_claims={"role": user.role}  # Adds the 'role' as a custom claim
        )
        return token
    @staticmethod
    def create_user(email, password, role, **kwargs):
        try:
            user = User(email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            user_profile = None

            if role == "volunteer":
                join_date_str = kwargs.pop('join_date', None)  # Remove join_date from kwargs
                join_date = None
                if join_date_str:
                    try:
                        join_date = datetime.fromisoformat(join_date_str.replace('Z', '+00:00'))
                    except ValueError:
                        db.session.rollback()
                        return None, "Invalid join_date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DDTHH:MM:SS+HH:MM)"
                user_profile = Volunteer(user_id=user.id, join_date=join_date, **kwargs)  # Pass join_date explicitly
            elif role == "commander":
                user_profile = Commander(user_id=user.id, **kwargs)
            elif role == "hr":
                user_profile = HR(user_id=user.id, **kwargs)
            else:
                db.session.rollback()
                return None, "Invalid Role"

            db.session.add(user_profile)
            db.session.commit()
            return user, None

        except Exception as e:
            db.session.rollback()
            return None, str(e)
    # @staticmethod
    # def create_user(email, password, role, **kwargs):
    #     try:
    #         user = User(email=email, role=role)
    #         user.set_password(password)
    #         db.session.add(user)
    #         db.session.commit()
    #
    #         user_profile = None # Initialize user profile
    #
    #         if role == "volunteer":
    #             # Convert join_date to datetime object
    #             join_date_str = kwargs.get('join_date')
    #             join_date = None
    #             if join_date_str:
    #                 try:
    #                     join_date = datetime.fromisoformat(join_date_str.replace('Z', '+00:00')) # Handle Z timezone
    #                 except ValueError:
    #                     db.session.rollback()
    #                     return None, "Invalid join_date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DDTHH:MM:SS+HH:MM)"
    #             user_profile = Volunteer(user_id=user.id, join_date=join_date, **kwargs)
    #         elif role == "commander":
    #             user_profile = Commander(user_id=user.id, **kwargs)
    #         elif role == "hr":
    #             user_profile = HR(user_id=user.id, **kwargs)
    #         else:
    #             db.session.rollback()
    #             return None, "Invalid Role"
    #
    #         db.session.add(user_profile)
    #         db.session.commit()
    #         return user, None
    #
    #     except Exception as e:
    #         db.session.rollback()
    #         return None, str(e)

    # @staticmethod
    # def create_user(email, password, role, **kwargs):
    #     try:
    #         user = User(email=email, role=role)
    #         user.set_password(password)
    #         db.session.add(user)
    #         db.session.commit()
    #
    #         if role == "volunteer":
    #             user_profile = Volunteer(user_id=user.id, **kwargs)
    #         elif role == "commander":
    #             user_profile = Commander(user_id=user.id, **kwargs)
    #         elif role == "hr":
    #             user_profile = HR(user_id=user.id, **kwargs)
    #         else:
    #             db.session.rollback()  # Rollback if role is invalid
    #             return None, "Invalid Role"
    #
    #         db.session.add(user_profile)
    #         db.session.commit()
    #         return user, None
    #     except Exception as e:
    #         db.session.rollback()
    #         return None, str(e)


# class AuthService:
#     @staticmethod
#     def login(email, password):
#         user = User.query.filter_by(email=email).first()
#         if user and user.check_password(password):
#             access_token = create_access_token(identity=user.id)
#             return access_token, user.role
#         return None, None
#
#     @staticmethod
#     def create_user(email, password, role, **kwargs):
#         user = User(email=email, role=role)
#         user.set_password(password)
#         return user

# Services


# curl -X POST \
#   http://127.0.0.1:5000/api/auth/login \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "email": "volunteer1@example.com",
#     "password": "volunteer_password_1"
#   }'

# curl -X POST \
#   http://127.0.0.1:5000/api/auth/login \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "email": "commander1@example.com",
#     "password": "commander_password_1"
#   }'

# curl -X POST \
#   http://127.0.0.1:5000/api/auth/login \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "email": "hr1@example.com",
#     "password": "hr_password_1"
#   }'

# curl -X POST \
#   http://127.0.0.1:5000/api/auth/login \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "email": "commander2@example.com",
#     "password": "commander_password_2"
#   }'

# curl -X POST \
#   http://127.0.0.1:5000/api/auth/login \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "email": "hr2@example.com",
#     "password": "hr_password_2"
#   }'

# curl -X POST \
#   http://127.0.0.1:5000/api/auth/login \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "email": "volunteer2@example.com",
#     "password": "volunteer_password_2"
#   }'

# curl -X POST \
#   http://127.0.0.1:5000/api/auth/login \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "email": "volunteer3@example.com",
#     "password": "volunteer_password_3"
#   }'
