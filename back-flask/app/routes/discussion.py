from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Question, DiscussionComment
from app.utils import role_required # Import role_required from utils

discussion_bp = Blueprint('discussion', __name__)

# Add a comment to a question's discussion (Any authenticated user)
@discussion_bp.route('/questions/<int:question_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(question_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    comment_text = data.get('comment_text')
    parent_comment_id = data.get('parent_comment_id') # For replies

    if not comment_text:
        return jsonify({"msg": "Comment text is required"}), 400

    question = Question.query.get(question_id)
    if not question:
        return jsonify({"msg": "Question not found"}), 404
    
    # Ensure question is deactivated before allowing comments (as per plan.md)
    if question.is_active:
        return jsonify({"msg": "Discussion is only available after question is deactivated"}), 403

    new_comment = DiscussionComment(
        question_id=question_id,
        user_id=current_user_id,
        comment_text=comment_text,
        parent_comment_id=parent_comment_id
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"msg": "Comment added successfully", "comment_id": new_comment.id}), 201

# Get all comments for a question's discussion
@discussion_bp.route('/questions/<int:question_id>/comments', methods=['GET'])
@jwt_required()
def get_comments(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"msg": "Question not found"}), 404
    
    # Only show comments if question is deactivated
    if question.is_active:
        return jsonify({"msg": "Discussion is only available after question is deactivated"}), 403

    # Fetch top-level comments first, then their replies
    top_level_comments = DiscussionComment.query.filter_by(question_id=question_id, parent_comment_id=None).order_by(DiscussionComment.timestamp.asc()).all()

    def format_comment(comment):
        user = User.query.get(comment.user_id)
        replies = [format_comment(reply) for reply in comment.replies]
        return {
            "id": comment.id,
            "user_id": comment.user_id,
            "username": user.username if user else "Unknown",
            "comment_text": comment.comment_text,
            "timestamp": comment.timestamp.isoformat(),
            "replies": replies
        }

    output = [format_comment(comment) for comment in top_level_comments]
    return jsonify(output), 200
