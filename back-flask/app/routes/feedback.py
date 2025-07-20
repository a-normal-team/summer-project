from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Feedback, Presentation
from app.utils import role_required # Import role_required from utils

feedback_bp = Blueprint('feedback', __name__)

# Submit Instant Feedback (Listener only)
@feedback_bp.route('/presentations/<int:presentation_id>/submit', methods=['POST'])
@role_required('listener')
def submit_feedback(presentation_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    feedback_type = data.get('feedback_type') # e.g., 'too_fast', 'too_slow', 'boring', 'bad_question'

    if not feedback_type:
        return jsonify({"msg": "Feedback type is required"}), 400

    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404
    
    # Ensure listener is associated with this presentation
    listener = User.query.get(int(current_user_id))
    if listener not in presentation.listeners:
        return jsonify({"msg": "You are not a listener for this presentation"}), 403

    new_feedback = Feedback(
        presentation_id=presentation_id,
        user_id=int(current_user_id),
        feedback_type=feedback_type
    )
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({"msg": "Feedback submitted successfully", "feedback_id": new_feedback.id}), 201

# Get Feedback Statistics for a Presentation (Speaker/Organizer)
@feedback_bp.route('/presentations/<int:presentation_id>/stats', methods=['GET'])
@jwt_required()
def get_feedback_stats(presentation_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    presentation = Presentation.query.get(presentation_id)

    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404
    
    # Only speaker of the presentation or organizer can view feedback stats
    if not (user.role.name == 'organizer' or (user.role.name == 'speaker' and presentation.speaker_id == int(current_user_id))):
        return jsonify({"msg": "Unauthorized to view feedback statistics"}), 403

    feedbacks = Feedback.query.filter_by(presentation_id=presentation_id).all()
    
    feedback_counts = {}
    for fb in feedbacks:
        feedback_counts[fb.feedback_type] = feedback_counts.get(fb.feedback_type, 0) + 1
    
    total_feedbacks = len(feedbacks)

    return jsonify({
        "presentation_id": presentation.id,
        "presentation_title": presentation.title,
        "total_feedbacks": total_feedbacks,
        "feedback_counts": feedback_counts
    }), 200
