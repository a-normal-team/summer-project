from flask import Blueprint, request, jsonify, current_app, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, File, Presentation
from app.utils import role_required, extract_text_from_file # Import extract_text_from_file
import uuid
import os
from io import BytesIO
# Removed base64 import as it's no longer needed for multipart/form-data

files_bp = Blueprint('files', __name__)

@files_bp.route('/upload', methods=['POST'])
@jwt_required()
@role_required('speaker') # Only speakers can upload files
def upload_file():
    if 'file' not in request.files:
        return jsonify({"msg": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400

    if file:
        s3_client = current_app.config.get('S3_CLIENT')
        s3_bucket_name = current_app.config.get('S3_BUCKET_NAME')

        if not s3_client or not s3_bucket_name:
            return jsonify({"msg": "S3/R2 storage not configured"}), 500

        original_filename = file.filename
        # Generate a unique key for S3
        file_extension = os.path.splitext(original_filename)[1]
        s3_key = f"{uuid.uuid4()}{file_extension}"

        try:
            # Read file content once
            file_content = file.read()
            file_stream_for_s3 = BytesIO(file_content) # Create a new stream for S3 upload

            # Upload file to S3/R2
            s3_client.upload_fileobj(file_stream_for_s3, s3_bucket_name, s3_key)

            current_user_id = int(get_jwt_identity()) # Convert to int for comparison
            user = User.query.get(current_user_id)
            current_app.logger.info(f"DEBUG: Current user ID: {current_user_id}, Role: {user.role.name}")

            # Optional: Link file to a presentation if presentation_id is provided
            presentation_id = request.form.get('presentation_id') # Get from form data
            current_app.logger.info(f"DEBUG: Received presentation_id from form: {presentation_id}")

            presentation = None
            if presentation_id:
                try:
                    presentation_id = int(presentation_id) # Ensure it's an integer
                except ValueError:
                    return jsonify({"msg": "Invalid presentation_id format"}), 400

                presentation = Presentation.query.get(presentation_id)
                if not presentation:
                    return jsonify({"msg": "Presentation not found"}), 404
                
                current_app.logger.info(f"DEBUG: Presentation found: ID={presentation.id}, Speaker ID={presentation.speaker_id}")

                # Ensure speaker owns the presentation if linking
                if presentation.speaker_id != current_user_id:
                    current_app.logger.warning(f"DEBUG: Unauthorized attempt: Presentation Speaker ID {presentation.speaker_id} != Current User ID {current_user_id}")
                    return jsonify({"msg": "You do not own this presentation"}), 403

            new_file = File(
                filename=original_filename,
                s3_key=s3_key,
                user_id=current_user_id,
                presentation_id=presentation_id,
                file_type=file.content_type,
                size=len(file_content) # Use length of read content
            )
            
            # Extract text content and store it
            extracted_text = extract_text_from_file(file_content, file.content_type) # Use file_content directly
            new_file.extracted_text_content = extracted_text

            db.session.add(new_file)
            db.session.commit()

            return jsonify({
                "msg": "File uploaded successfully",
                "file_id": new_file.id,
                "filename": new_file.filename,
                "s3_key": new_file.s3_key
            }), 201

        except Exception as e:
            current_app.logger.error(f"Error uploading file and extracting text: {e}")
            return jsonify({"msg": f"Failed to upload file or extract text: {str(e)}"}), 500
    return jsonify({"msg": "File upload failed"}), 400 # This line was missing in the original, but good to have a fallback

@files_bp.route('/download/<int:file_id>', methods=['GET'])
@jwt_required()
def download_file(file_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    file_record = File.query.get(file_id)
    if not file_record:
        return jsonify({"msg": "File not found"}), 404

    # Authorization check: Only organizer or listener can download
    # Or if the user is the speaker who uploaded it
    if user.role.name not in ['organizer', 'listener'] and user.id != file_record.user_id:
        return jsonify({"msg": "Unauthorized to download this file"}), 403

    s3_client = current_app.config.get('S3_CLIENT')
    s3_bucket_name = current_app.config.get('S3_BUCKET_NAME')

    if not s3_client or not s3_bucket_name:
        return jsonify({"msg": "S3/R2 storage not configured"}), 500

    try:
        file_object = s3_client.get_object(Bucket=s3_bucket_name, Key=file_record.s3_key)
        file_content = file_object['Body'].read()

        return send_file(
            BytesIO(file_content),
            mimetype=file_record.file_type or 'application/octet-stream',
            as_attachment=True,
            download_name=file_record.filename
        )
    except s3_client.exceptions.NoSuchKey:
        return jsonify({"msg": "File not found in storage"}), 404
    except Exception as e:
        current_app.logger.error(f"Error downloading file from S3: {e}")
        return jsonify({"msg": f"Failed to download file: {str(e)}"}), 500

@files_bp.route('/files_by_presentation/<int:presentation_id>', methods=['GET'])
@jwt_required()
def get_files_by_presentation(presentation_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404

    # Authorization check: Only speaker of the presentation, organizer, or listener can view files
    if user.id != presentation.speaker_id and user.role.name not in ['organizer', 'listener']:
        return jsonify({"msg": "Unauthorized to view files for this presentation"}), 403

    files = File.query.filter_by(presentation_id=presentation_id).all()
    file_list = [{
        "id": f.id,
        "filename": f.filename,
        "upload_date": f.upload_date.isoformat(),
        "user_id": f.user_id,
        "file_type": f.file_type,
        "size": f.size
    } for f in files]

    return jsonify(file_list), 200

@files_bp.route('/delete/<int:file_id>', methods=['DELETE'])
@jwt_required()
def delete_file(file_id):
    """
    删除文件接口 - 仅限组织者和文件上传者（演讲者）使用
    """
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    # 查找文件记录
    file_record = File.query.get(file_id)
    if not file_record:
        return jsonify({"msg": "File not found"}), 404
        
    # 权限检查：只有组织者和文件上传者可以删除文件
    if not (user.role.name == 'organizer' or file_record.user_id == current_user_id):
        return jsonify({"msg": "Unauthorized to delete this file"}), 403
    
    try:
        # 1. 从S3/R2存储中删除文件
        s3_client = current_app.config.get('S3_CLIENT')
        s3_bucket_name = current_app.config.get('S3_BUCKET_NAME')
        
        if not s3_client or not s3_bucket_name:
            return jsonify({"msg": "S3/R2 storage not configured"}), 500
            
        # 尝试删除对象存储中的文件
        try:
            s3_client.delete_object(Bucket=s3_bucket_name, Key=file_record.s3_key)
        except Exception as e:
            current_app.logger.error(f"Error deleting file from S3/R2: {e}")
            # 即使从S3/R2删除失败，我们也继续删除数据库记录
        
        # 2. 从数据库中删除文件记录
        db.session.delete(file_record)
        db.session.commit()
        
        return jsonify({"msg": "File deleted successfully"}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error deleting file: {e}")
        db.session.rollback()
        return jsonify({"msg": f"Failed to delete file: {str(e)}"}), 500
