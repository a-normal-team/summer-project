from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
import PyPDF2 # Add this import
from io import BytesIO # Add this import

def role_required(role_name):
    def wrapper(fn):
        @wraps(fn) # Preserve original function's metadata
        @jwt_required()
        def decorator(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if user and user.role.name == role_name:
                return fn(*args, **kwargs)
            return jsonify({"msg": f"'{role_name}' role required"}), 403
        return decorator
    return wrapper

def extract_text_from_file(file_content_bytes, file_type):
    """
    Extracts text content from a file (PDF or plain text).
    :param file_content_bytes: Bytes content of the file.
    :param file_type: MIME type of the file (e.g., 'application/pdf', 'text/plain').
    :return: Extracted text as a string.
    """
    if file_type == 'application/pdf':
        try:
            pdf_file = BytesIO(file_content_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text() or ""
            return text
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {e}")
    elif file_type.startswith('text/'):
        try:
            return file_content_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return file_content_bytes.decode('latin-1') # Fallback for other encodings
    else:
        raise ValueError(f"Unsupported file type for text extraction: {file_type}")
