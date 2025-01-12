from flask import Flask
from flask_jwt_extended import JWTManager
from db import db
from config import Config
import os
from flask_cors import CORS

from models import User, Volunteer, Resume, Commander, HR, Job, JobQuestion, JobApplication, ApplicationAnswer, Interview


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    # CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:4200", "http://127.0.0.1:4200"]}}, supports_credentials=True)

    # Register blueprints
    from controllers.auth_controller import auth_bp
    from controllers.volunteer_controller import volunteer_bp
    from controllers.commander_controller import commander_bp
    from controllers.hr_controller import hr_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(volunteer_bp, url_prefix='/api/volunteer')
    app.register_blueprint(commander_bp, url_prefix='/api/commander')
    app.register_blueprint(hr_bp, url_prefix='/api/hr')

    # Create upload directories
    os.makedirs(os.path.join('uploads', 'resumes'), exist_ok=True)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        try:
            print("Creating all tables...")
            db.create_all()
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")
    app.run(debug=True)
