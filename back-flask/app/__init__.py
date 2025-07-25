from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # 导入CORS
import os
import boto3 # Add this import
from flask_socketio import SocketIO # Add this import
from datetime import timedelta # Add this import
import logging # 导入日志模块

# 配置日志
logging.basicConfig(level=logging.INFO)

# Move model import here to ensure models are loaded before db.init_app
from .models import Role, User, Presentation, Question, Answer, Feedback, DiscussionComment, File

bcrypt = Bcrypt()
jwt = JWTManager()
socketio = SocketIO(
    cors_allowed_origins="*",  # 允许所有源
    always_connect=True,      # 即使握手失败也建立连接
    logger=True,              # 启用日志
    engineio_logger=True      # 启用Engine.IO日志
) # Initialize SocketIO with CORS support

def create_app():
    app = Flask(__name__)
    from .models import db # Import db from models to avoid circular import
    db.init_app(app) # Initialize db with the app
    
    # 配置CORS - 确保前端可以正常访问，特别是WebSocket连接
    # 使用通配符允许所有来源
    
    cors_config = {
        'origins': '*',  # 允许所有来源
        'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],  # 允许所有常用HTTP方法
        'allow_headers': '*',  # 允许所有请求头，简化配置
        'expose_headers': ['Content-Type', 'Authorization'],  # 允许前端访问这些响应头
        'supports_credentials': False,  # 不携带凭证(cookies等)
    }
    CORS(app, **cors_config)  # 使用配置初始化CORS
    
    # 动态设置响应头，确保CORS正常工作
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')  # 允许所有请求头
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        # 不设置 Access-Control-Allow-Credentials，因为我们使用的是通配符来源
        return response

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 明确设置为False以避免警告
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
    
    # 初始化并配置SocketIO
    socketio.init_app(
        app, 
        cors_allowed_origins="*",  # 允许所有来源
        always_connect=True,     # 即使握手失败也建立连接
        cors_credentials=False   # 不携带凭证，与通配符来源配合使用
    ) # Initialize SocketIO with app
    from app.utils.websocket import init_socketio
    init_socketio(socketio) # 注册WebSocket事件处理程序

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

    return app # 只返回app，socketio已经全局可用
