from flask import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os
import boto3 # Add this import
from flask_socketio import SocketIO # Add this import
from datetime import timedelta # Add this import

# Move model import here to ensure models are loaded before db.init_app
from .models import Role, User, Presentation, Question, Answer, Feedback, DiscussionComment, File

bcrypt = Bcrypt()
jwt = JWTManager()
socketio = SocketIO() # Initialize SocketIO

def create_app():
    app = Flask(__name__)
    from .models import db # Import db from models to avoid circular import
    db.init_app(app) # Initialize db with the app

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24) # Set token expiration to 24 hours

    # LLM API Configuration
    app.config['LLM_API_URL'] = os.environ.get('LLM_API_URL')
    app.config['DEEPSEEK_API_KEY'] = os.environ.get('DEEPSEEK_API_KEY') # Add this line

    # S3/R2 Configuration
    app.config['S3_ENDPOINT_URL'] = os.environ.get('S3_ENDPOINT_URL')
    app.config['S3_ACCESS_KEY_ID'] = os.environ.get('S3_ACCESS_KEY_ID')
    app.config['S3_SECRET_ACCESS_KEY'] = os.environ.get('S3_SECRET_ACCESS_KEY')
    app.config['S3_BUCKET_NAME'] = os.environ.get('S3_BUCKET_NAME')

    # Initialize S3 client
    if app.config['S3_ENDPOINT_URL'] and app.config['S3_ACCESS_KEY_ID'] and app.config['S3_SECRET_ACCESS_KEY']:
        s3_client = boto3.client(
            's3',
            endpoint_url=app.config['S3_ENDPOINT_URL'],
            aws_access_key_id=app.config['S3_ACCESS_KEY_ID'],
            aws_secret_access_key=app.config['S3_SECRET_ACCESS_KEY']
        )
        app.config['S3_CLIENT'] = s3_client
    else:
        app.config['S3_CLIENT'] = None # Or raise an error if S3 is mandatory

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*") # Initialize SocketIO with app

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.presentations import presentations_bp
    from .routes.quiz import quiz_bp
    from .routes.feedback import feedback_bp
    from .routes.discussion import discussion_bp
    from .routes.files import files_bp # Import new blueprint

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(presentations_bp, url_prefix='/api/presentations')
    app.register_blueprint(quiz_bp, url_prefix='/api/quiz')
    app.register_blueprint(feedback_bp, url_prefix='/api/feedback')
    app.register_blueprint(discussion_bp, url_prefix='/api/discussion')
    app.register_blueprint(files_bp, url_prefix='/api/files') # Register new blueprint

    return app, socketio # Return socketio object as well
