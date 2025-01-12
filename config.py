import os
from datetime import timedelta

# class Config:
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///volunteer_system.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
#     JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class Config:
    # Absolute path to the database file
    db_path = os.path.join(os.getcwd(), 'volunteer_system.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key' # Use SECRET_KEY for JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)