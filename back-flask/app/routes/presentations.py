from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Presentation, Role
from app.utils import role_required
from app import socketio # Import socketio
from flask_socketio import join_room, leave_room, emit # Import join_room, leave_room, emit

presentations_bp = Blueprint('presentations', __name__)

@socketio.on('join_presentation')
@jwt_required()
def handle_join_presentation(data):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    presentation_id = data.get('presentation_id')

    if not presentation_id:
        emit('error', {'msg': 'Presentation ID is required'}, room=request.sid)
        return

    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        emit('error', {'msg': 'Presentation not found'}, room=request.sid)
        return

    # Check if user is authorized to join this presentation's room
    # Speaker of the presentation, or a listener associated with it, or an organizer
    if not (user.id == presentation.speaker_id or user in presentation.listeners or user.role.name == 'organizer'):
        emit('error', {'msg': 'Unauthorized to join this presentation room'}, room=request.sid)
        return

    room = f'presentation_{presentation_id}'
    join_room(room)
    emit('status', {'msg': f'Joined presentation room {presentation_id}'}, room=request.sid)
    current_app.logger.info(f"User {user.username} joined room {room}")

@socketio.on('leave_presentation')
@jwt_required()
def handle_leave_presentation(data):
    current_user_id = get_jwt_identity()
    # user = User.query.get(current_user_id) # Unused variable
    presentation_id = data.get('presentation_id')

    if not presentation_id:
        emit('error', {'msg': 'Presentation ID is required'}, room=request.sid)
        return

    room = f'presentation_{presentation_id}'
    leave_room(room)
    emit('status', {'msg': f'Left presentation room {presentation_id}'}, room=request.sid)
    current_app.logger.info(f"User {current_user_id} left room {room}")

# Create Presentation (Speaker only)
@presentations_bp.route('/', methods=['POST'])
@role_required('speaker')
def create_presentation():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({"msg": "Title is required"}), 400

    new_presentation = Presentation(title=title, description=description, speaker_id=current_user_id)
    db.session.add(new_presentation)
    db.session.commit()
    return jsonify({"msg": "Presentation created successfully", "presentation_id": new_presentation.id}), 201

# Get All Presentations
@presentations_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_presentations():
    presentations = Presentation.query.all()
    output = []
    for p in presentations:
        output.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "speaker": p.speaker.username
        })
    return jsonify(output), 200

# Get Presentation by ID
@presentations_bp.route('/<int:presentation_id>', methods=['GET'])
@jwt_required()
def get_presentation(presentation_id):
    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404
    
    return jsonify({
        "id": presentation.id,
        "title": presentation.title,
        "description": presentation.description,
        "speaker": presentation.speaker.username,
        "listeners": [{"id": l.id, "username": l.username} for l in presentation.listeners]
    }), 200

# Update Presentation (Speaker or Organizer only)
@presentations_bp.route('/<int:presentation_id>', methods=['PUT'])
@jwt_required()
def update_presentation(presentation_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404

    # Only the speaker of the presentation or an organizer can update it
    if not (user.id == presentation.speaker_id or user.role.name == 'organizer'):
        return jsonify({"msg": "Unauthorized to update this presentation"}), 403

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if title:
        presentation.title = title
    if description:
        presentation.description = description
    
    db.session.commit()
    return jsonify({"msg": "Presentation updated successfully"}), 200

# Add Listener to Presentation (Organizer or Speaker)
@presentations_bp.route('/<int:presentation_id>/add_listener', methods=['POST'])
@jwt_required()
def add_listener_to_presentation(presentation_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id) # Used for role check

    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404

    # 允许三种情况：1.组织者添加任何听众；2.演讲者添加任何听众；3.听众添加自己
    if user.role.name == 'listener':
        # 听众只能添加自己
        listener = user  # 使用当前用户作为听众
    else:
        # 组织者或演讲者可以添加指定的听众
        data = request.get_json()
        listener_id = data.get('listener_id')
        if not listener_id:
            return jsonify({"msg": "Listener ID is required"}), 400
        
        listener = User.query.get(listener_id)
        if not listener or listener.role.name != 'listener':
            return jsonify({"msg": "Listener not found or not a listener role"}), 404
    
    # 权限检查：组织者可以添加任何听众，演讲者只能添加到自己的演讲，听众只能添加自己
    if user.role.name == 'organizer' or (user.role.name == 'speaker' and presentation.speaker_id == int(current_user_id)) or (user.role.name == 'listener' and user.id == listener.id):
        if listener not in presentation.listeners:
            presentation.listeners.append(listener)
            db.session.commit()
            return jsonify({"msg": "Listener added to presentation successfully"}), 200
        return jsonify({"msg": "Listener already associated with this presentation"}), 409
    return jsonify({"msg": "Unauthorized to add listener to this presentation"}), 403

# Remove Listener from Presentation (Organizer or Speaker)
@presentations_bp.route('/<int:presentation_id>/remove_listener', methods=['POST'])
@jwt_required()
def remove_listener_from_presentation(presentation_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id) # Used for role check

    data = request.get_json()
    listener_id = data.get('listener_id')

    presentation = Presentation.query.get(presentation_id)
    listener = User.query.get(listener_id)

    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404
    if not listener or listener.role.name != 'listener':
        return jsonify({"msg": "Listener not found or not a listener role"}), 404
    
    # Only organizer or the speaker of the presentation can remove listeners
    if user.role.name == 'organizer' or (user.role.name == 'speaker' and presentation.speaker_id == int(current_user_id)):
        if listener in presentation.listeners:
            presentation.listeners.remove(listener)
            db.session.commit()
            return jsonify({"msg": "Listener removed from presentation successfully"}), 200
        return jsonify({"msg": "Listener not associated with this presentation"}), 409
    return jsonify({"msg": "Unauthorized to remove listener from this presentation"}), 403

# Delete Presentation (Speaker or Organizer only)
@presentations_bp.route('/<int:presentation_id>', methods=['DELETE'])
@jwt_required()
def delete_presentation(presentation_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404

    # Only the speaker of the presentation or an organizer can delete it
    if not (user.id == presentation.speaker_id or user.role.name == 'organizer'):
        return jsonify({"msg": "Unauthorized to delete this presentation"}), 403

    db.session.delete(presentation)
    db.session.commit()
    return jsonify({"msg": "Presentation deleted successfully"}), 200
