from flask import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os
import boto3 # Add this import
from flask_socketio import SocketIO # Add this import

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
socketio = SocketIO() # Initialize SocketIO

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')

    # LLM API Configuration
    app.config['LLM_API_URL'] = os.environ.get('LLM_API_URL')

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

    from .models import Role, User, Presentation, Question, Answer, Feedback, DiscussionComment, File # Add File model

    # Database initialization
    @app.before_first_request
    def create_tables():
        db.create_all()
        # Initialize roles if they don't exist
        if not Role.query.filter_by(name='organizer').first():
            db.session.add(Role(name='organizer'))
        if not Role.query.filter_by(name='speaker').first():
            db.session.add(Role(name='speaker'))
        if not Role.query.filter_by(name='listener').first():
            db.session.add(Role(name='listener'))
        db.session.commit()

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
