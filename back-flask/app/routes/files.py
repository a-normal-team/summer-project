from flask import Blueprint, request, jsonify, current_app, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, File, Presentation
from app.utils import role_required, extract_text_from_file # Import extract_text_from_file
import uuid
import os
from io import BytesIO

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
            # Upload file to S3/R2
            s3_client.upload_fileobj(file, s3_bucket_name, s3_key)

            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)

            # Optional: Link file to a presentation if presentation_id is provided
            presentation_id = request.form.get('presentation_id')
            presentation = None
            if presentation_id:
                presentation = Presentation.query.get(presentation_id)
                if not presentation:
                    return jsonify({"msg": "Presentation not found"}), 404
                # Ensure speaker owns the presentation if linking
                if presentation.speaker_id != current_user_id:
                    return jsonify({"msg": "You do not own this presentation"}), 403

            new_file = File(
                filename=original_filename,
                s3_key=s3_key,
                user_id=current_user_id,
                presentation_id=presentation_id,
                file_type=file.content_type,
                size=file.content_length # This might not be accurate for all file types, but good for basic check
            )
            
            # Extract text content and store it
            file.seek(0) # Reset file pointer after S3 upload
            extracted_text = extract_text_from_file(file.read(), file.content_type)
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
    return jsonify({"msg": "File upload failed"}), 400

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
