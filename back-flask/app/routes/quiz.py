from flask import Blueprint, request, jsonify, current_app # Add current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Question, Answer, Presentation, Role, File # Add File
from app.utils import role_required, extract_text_from_file # Import extract_text_from_file
import json
import requests # Add this import
from app import socketio # Import socketio
from flask_socketio import emit # Import emit

quiz_bp = Blueprint('quiz', __name__)

# Create Question (Speaker only)
@quiz_bp.route('/presentations/<int:presentation_id>/questions', methods=['POST'])
@role_required('speaker')
def create_question(presentation_id):
    current_user_id = get_jwt_identity()
    presentation = Presentation.query.get(presentation_id)

    if not presentation or presentation.speaker_id != current_user_id:
        return jsonify({"msg": "Presentation not found or you are not the speaker"}), 404

    data = request.get_json()
    question_text = data.get('question_text')
    question_type = data.get('question_type', 'multiple_choice')
    options = data.get('options') # List of strings
    correct_answer = data.get('correct_answer')

    if not question_text:
        return jsonify({"msg": "Question text is required"}), 400
    
    if question_type == 'multiple_choice' and not options:
        return jsonify({"msg": "Options are required for multiple choice questions"}), 400

    new_question = Question(
        presentation_id=presentation_id,
        question_text=question_text,
        question_type=question_type,
        options=json.dumps(options) if options else None,
        correct_answer=correct_answer,
        is_active=True # New questions are active by default
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({"msg": "Question created successfully", "question_id": new_question.id}), 201

# Get Active Question for a Presentation (Listener/Speaker)
@quiz_bp.route('/presentations/<int:presentation_id>/active_question', methods=['GET'])
@jwt_required()
def get_active_question(presentation_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404

    # Check if user is a listener or the speaker of this presentation
    if user.role.name == 'listener' and user not in presentation.listeners:
        return jsonify({"msg": "You are not a listener for this presentation"}), 403
    if user.role.name == 'speaker' and presentation.speaker_id != current_user_id:
        return jsonify({"msg": "You are not the speaker for this presentation"}), 403
    
    active_question = Question.query.filter_by(presentation_id=presentation_id, is_active=True).first()
    if not active_question:
        return jsonify({"msg": "No active question for this presentation"}), 404
    
    return jsonify({
        "id": active_question.id,
        "question_text": active_question.question_text,
        "question_type": active_question.question_type,
        "options": json.loads(active_question.options) if active_question.options else None
    }), 200

# Submit Answer (Listener only)
@quiz_bp.route('/questions/<int:question_id>/answer', methods=['POST'])
@role_required('listener')
def submit_answer(question_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    answer_text = data.get('answer_text')

    question = Question.query.get(question_id)
    if not question or not question.is_active:
        return jsonify({"msg": "Question not found or not active"}), 404

    # Check if listener has already answered this question
    existing_answer = Answer.query.filter_by(question_id=question_id, user_id=current_user_id).first()
    if existing_answer:
        return jsonify({"msg": "You have already answered this question"}), 409

    is_correct = None
    if question.correct_answer:
        is_correct = (answer_text == question.correct_answer)

    new_answer = Answer(
        question_id=question_id,
        user_id=current_user_id,
        answer_text=answer_text,
        is_correct=is_correct
    )
    db.session.add(new_answer)
    db.session.commit()

    response = {"msg": "Answer submitted successfully", "answer_id": new_answer.id}
    if is_correct is not None:
        response["is_correct"] = is_correct
    
    # Emit answer update for real-time stats
    # Get updated stats for the question
    question_stats = get_question_stats(question_id).json # Call the existing stats function
    socketio.emit('question_stats_update', question_stats, room=f'presentation_{question.presentation_id}')

    return jsonify(response), 201

# Deactivate Question (Speaker only)
@quiz_bp.route('/questions/<int:question_id>/deactivate', methods=['POST'])
@role_required('speaker')
def deactivate_question(question_id):
    current_user_id = get_jwt_identity()
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"msg": "Question not found"}), 404
    
    # Ensure the speaker owns the presentation this question belongs to
    presentation = Presentation.query.get(question.presentation_id)
    if not presentation or presentation.speaker_id != current_user_id:
        return jsonify({"msg": "Unauthorized to deactivate this question"}), 403

    question.is_active = False
    db.session.commit()
    return jsonify({"msg": "Question deactivated successfully"}), 200

# Get Question Statistics (Speaker/Organizer)
@quiz_bp.route('/questions/<int:question_id>/stats', methods=['GET'])
@jwt_required()
def get_question_stats(question_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"msg": "Question not found"}), 404
    
    presentation = Presentation.query.get(question.presentation_id)
    # Only speaker of the presentation or organizer can view stats
    if not (user.role.name == 'organizer' or (user.role.name == 'speaker' and presentation.speaker_id == current_user_id)):
        return jsonify({"msg": "Unauthorized to view question statistics"}), 403

    total_answers = Answer.query.filter_by(question_id=question_id).count()
    correct_answers = Answer.query.filter_by(question_id=question_id, is_correct=True).count()
    
    correct_rate = (correct_answers / total_answers * 100) if total_answers > 0 else 0

    # Option distribution for multiple choice questions
    option_distribution = {}
    if question.question_type == 'multiple_choice' and question.options:
        answers = Answer.query.filter_by(question_id=question_id).all()
        for answer in answers:
            option_distribution[answer.answer_text] = option_distribution.get(answer.answer_text, 0) + 1

    return jsonify({
        "question_id": question.id,
        "question_text": question.question_text,
        "total_answers": total_answers,
        "correct_answers": correct_answers,
        "correct_rate": f"{correct_rate:.2f}%",
        "option_distribution": option_distribution
    }), 200

# Get Listener's Report for a Presentation (Listener/Organizer)
@quiz_bp.route('/presentations/<int:presentation_id>/report/<int:user_id>', methods=['GET'])
@jwt_required()
def get_listener_report(presentation_id, user_id):
    current_user_id = get_jwt_identity()
    requester = User.query.get(current_user_id)
    listener = User.query.get(user_id)

    if not listener or listener.role.name != 'listener':
        return jsonify({"msg": "User is not a listener"}), 404

    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404

    # Listener can only view their own report, Organizer can view any listener's report
    if not (requester.role.name == 'organizer' or (requester.role.name == 'listener' and requester.id == user_id)):
        return jsonify({"msg": "Unauthorized to view this report"}), 403

    questions = Question.query.filter_by(presentation_id=presentation_id).all()
    total_questions = len(questions)
    correct_answers_count = 0
    answered_questions_count = 0
    
    question_details = []

    for q in questions:
        answer = Answer.query.filter_by(question_id=q.id, user_id=user_id).first()
        detail = {
            "question_id": q.id,
            "question_text": q.question_text,
            "your_answer": answer.answer_text if answer else None,
            "is_correct": answer.is_correct if answer else None,
            "correct_answer": q.correct_answer # Include correct answer in report
        }
        question_details.append(detail)

        if answer:
            answered_questions_count += 1
            if answer.is_correct:
                correct_answers_count += 1
    
    accuracy_rate = (correct_answers_count / answered_questions_count * 100) if answered_questions_count > 0 else 0

    return jsonify({
        "listener_id": listener.id,
        "listener_username": listener.username,
        "presentation_id": presentation.id,
        "presentation_title": presentation.title,
        "total_questions_in_presentation": total_questions,
        "answered_questions": answered_questions_count,
        "correct_answers": correct_answers_count,
        "accuracy_rate": f"{accuracy_rate:.2f}%",
        "question_details": question_details
    }), 200

# Get Overall Presentation Statistics (Organizer)
@quiz_bp.route('/presentations/<int:presentation_id>/overall_stats', methods=['GET'])
@role_required('organizer')
def get_overall_presentation_stats(presentation_id):
    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404

    total_listeners = presentation.listeners.count() # Count listeners associated with this presentation
    
    all_questions = Question.query.filter_by(presentation_id=presentation_id).all()
    total_questions_in_presentation = len(all_questions)

    total_answers_across_all_questions = 0
    total_correct_answers_across_all_questions = 0

    for q in all_questions:
        total_answers_across_all_questions += Answer.query.filter_by(question_id=q.id).count()
        total_correct_answers_across_all_questions += Answer.query.filter_by(question_id=q.id, is_correct=True).count()

    average_correct_rate = (total_correct_answers_across_all_questions / total_answers_across_all_questions * 100) if total_answers_across_all_questions > 0 else 0

    # Get individual listener performance
    listener_performance = []
    for listener in presentation.listeners:
        listener_report = get_listener_report(presentation_id, listener.id).json # Call the existing report function
        listener_performance.append({
            "listener_id": listener.id,
            "listener_username": listener.username,
            "answered_questions": listener_report.get('answered_questions'),
            "correct_answers": listener_report.get('correct_answers'),
            "accuracy_rate": listener_report.get('accuracy_rate')
        })

    return jsonify({
        "presentation_id": presentation.id,
        "presentation_title": presentation.title,
        "total_participants": total_listeners,
        "total_questions_in_presentation": total_questions_in_presentation,
        "total_answers_submitted": total_answers_across_all_questions,
        "average_correct_rate_across_all_questions": f"{average_correct_rate:.2f}%",
        "listener_performance": listener_performance
    }), 200

@quiz_bp.route('/generate_questions', methods=['POST'])
@jwt_required()
@role_required('speaker') # Only speakers can generate questions
def generate_questions():
    data = request.get_json()
    file_id = data.get('file_id')
    presentation_id = data.get('presentation_id') # Assuming questions are linked to a presentation

    if not file_id or not presentation_id:
        return jsonify({"msg": "file_id and presentation_id are required"}), 400

    # Predefined prompt based on user requirements
    prompt = "请根据提供的文本内容，生成高质量的单项选择题。每个问题应具有深度，字数不少于60字。每个选项的答案字数长度不少于20字。请确保每个问题只有一个正确答案。"

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    file_record = File.query.get(file_id)
    if not file_record:
        return jsonify({"msg": "File not found"}), 404

    # Ensure the speaker owns the file or the presentation it's linked to
    if file_record.user_id != current_user_id:
        # If file is linked to a presentation, check if speaker owns that presentation
        if file_record.presentation_id and file_record.presentation.speaker_id == current_user_id:
            pass # OK, speaker owns the presentation
        else:
            return jsonify({"msg": "Unauthorized to use this file"}), 403

    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404
    if presentation.speaker_id != current_user_id:
        return jsonify({"msg": "You are not the speaker of this presentation"}), 403

    s3_client = current_app.config.get('S3_CLIENT')
    s3_bucket_name = current_app.config.get('S3_BUCKET_NAME')
    llm_api_url = current_app.config.get('LLM_API_URL')

    if not s3_client or not s3_bucket_name:
        return jsonify({"msg": "S3/R2 storage not configured"}), 500
    if not llm_api_url:
        return jsonify({"msg": "LLM API URL not configured"}), 500

    try:
        # Download file content from S3
        file_object = s3_client.get_object(Bucket=s3_bucket_name, Key=file_record.s3_key)
        file_content_bytes = file_object['Body'].read()

        # Use extracted_text_content from the database
        extracted_text = file_record.extracted_text_content
        if not extracted_text:
            return jsonify({"msg": "No extracted text content found for this file"}), 400

        # Step 1: Summarize the extracted text using LLM
        summary_prompt = "请对以下文本进行精简总结，提取核心要点，用于后续生成测验题目。总结应简洁明了，保留关键信息。"
        summary_payload = {
            "text_content": extracted_text,
            "prompt": summary_prompt
        }
        current_app.logger.info("Calling LLM API for summarization...")
        summary_response = requests.post(llm_api_url, json=summary_payload)
        summary_response.raise_for_status()
        summarized_text = summary_response.json().get('summary', extracted_text) # Assuming LLM returns {'summary': '...'}

        current_app.logger.info(f"Summarized text length: {len(summarized_text)}")

        # Step 2: Generate questions based on the summarized text and user's prompt
        llm_payload = {
            "text_content": summarized_text,
            "prompt": prompt # Use the user's original prompt for question generation
        }

        current_app.logger.info("Calling LLM API for question generation...")
        llm_response = requests.post(llm_api_url, json=llm_payload)
        llm_response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        generated_questions_data = llm_response.json()

        # Assuming LLM returns a list of questions, each with 'question_text', 'question_type', 'options', 'correct_answer'
        # Example LLM response format:
        # [
        #   {
        #     "question_text": "...",
        #     "question_type": "multiple_choice",
        #     "options": ["...", "..."],
        #     "correct_answer": "..."
        #   },
        #   ...
        # ]

        new_questions = []
        for q_data in generated_questions_data:
            question_text = q_data.get('question_text')
            question_type = q_data.get('question_type', 'multiple_choice')
            options = q_data.get('options')
            correct_answer = q_data.get('correct_answer')

            if not question_text:
                current_app.logger.warning("LLM returned a question without 'question_text'. Skipping.")
                continue

            new_question = Question(
                presentation_id=presentation_id,
                question_text=question_text,
                question_type=question_type,
                options=json.dumps(options) if options else None,
                correct_answer=correct_answer,
                is_active=False # Questions are inactive by default, speaker activates them later
            )
        db.session.add(new_question)
        new_questions.append(new_question)

        db.session.commit()

        # Emit new question to listeners in the presentation room
        # Assuming a room for each presentation, e.g., 'presentation_<id>'
        question_data = {
            "id": new_question.id,
            "question_text": new_question.question_text,
            "question_type": new_question.question_type,
            "options": json.loads(new_question.options) if new_question.options else None,
            "is_active": new_question.is_active
        }
        socketio.emit('new_question', question_data, room=f'presentation_{presentation_id}')

        return jsonify({
            "msg": f"Successfully generated {len(new_questions)} questions",
            "question_ids": [q.id for q in new_questions]
        }), 201

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error calling LLM API: {e}")
        return jsonify({"msg": f"Failed to generate questions from LLM: {str(e)}"}), 500
    except ValueError as e: # For file extraction errors
        current_app.logger.error(f"File extraction error: {e}")
        return jsonify({"msg": f"File processing error: {str(e)}"}), 400
    except Exception as e:
        current_app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"msg": f"An unexpected error occurred: {str(e)}"}), 500
