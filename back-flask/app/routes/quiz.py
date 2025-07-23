from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Question, Answer, Presentation, Role, File
from app.utils import role_required, extract_text_from_file
import json
import requests
from app import socketio
from flask_socketio import emit
from openai import OpenAI # Import OpenAI

quiz_bp = Blueprint('quiz', __name__)

# Create Question (Speaker only)
@quiz_bp.route('/presentations/<int:presentation_id>/questions', methods=['POST'])
@role_required('speaker')
def create_question(presentation_id):
    current_user_id = get_jwt_identity()
    presentation = Presentation.query.get(presentation_id)

    if not presentation or presentation.speaker_id != int(current_user_id):
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
@quiz_bp.route('/presentations/<int:presentation_id>/questions', methods=['GET'])
@jwt_required()
def get_presentation_questions(presentation_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404
    
    # 检查用户是否有权限访问该演示文稿
    if user.role.name == 'listener' and user not in presentation.listeners:
        return jsonify({"msg": "You are not a listener for this presentation"}), 403
    if user.role.name == 'speaker' and presentation.speaker_id != int(current_user_id):
        return jsonify({"msg": "You are not the speaker for this presentation"}), 403
    
    # 获取演示文稿的所有问题
    questions = Question.query.filter_by(presentation_id=presentation_id).all()
    
    # 将问题转换为JSON格式
    question_list = []
    for q in questions:
        question_data = {
            "id": q.id,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "options": json.loads(q.options) if q.options else None,
            "is_active": q.is_active
        }
        # 只有演讲者和组织者可以看到正确答案
        if user.role.name in ['speaker', 'organizer']:
            question_data["correct_answer"] = q.correct_answer
        
        question_list.append(question_data)
    
    return jsonify({"questions": question_list}), 200

@quiz_bp.route('/presentations/<int:presentation_id>/active_questions', methods=['GET'])
@jwt_required()
def get_active_questions(presentation_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404

    # 检查用户是否有权限访问该演示文稿
    if user.role.name == 'listener' and user not in presentation.listeners:
        return jsonify({"msg": "You are not a listener for this presentation"}), 403
    if user.role.name == 'speaker' and presentation.speaker_id != int(current_user_id):
        return jsonify({"msg": "You are not the speaker for this presentation"}), 403
    
    # 获取演示文稿的所有活跃问题
    active_questions = Question.query.filter_by(presentation_id=presentation_id, is_active=True).all()
    
    # 将问题转换为JSON格式
    active_question_list = []
    for q in active_questions:
        question_data = {
            "id": q.id,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "options": json.loads(q.options) if q.options else None
        }
        active_question_list.append(question_data)
    
    if not active_question_list:
        return jsonify({"active_questions": [], "msg": "No active questions for this presentation"}), 200
    
    return jsonify({"active_questions": active_question_list}), 200

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
    if user.role.name == 'speaker' and presentation.speaker_id != int(current_user_id):
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
    
    # 注释WebSocket相关代码 - 暂时不使用实时广播功能
    # # Emit answer update for real-time stats
    # # Get updated stats for the question
    # question_stats = _get_question_stats_data(question_id) # Call the helper function
    # if question_stats: # Ensure stats were retrieved successfully
    #     socketio.emit('question_stats_update', question_stats, room=f'presentation_{question.presentation_id}')

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
    if not presentation or presentation.speaker_id != int(current_user_id):
        return jsonify({"msg": "Unauthorized to deactivate this question"}), 403

    question.is_active = False
    db.session.commit()
    return jsonify({"msg": "Question deactivated successfully"}), 200

def _get_question_stats_data(question_id):
    """Helper function to get question statistics data as a dictionary."""
    question = Question.query.get(question_id)
    if not question:
        return None # Or raise an exception, depending on desired error handling

    total_answers = Answer.query.filter_by(question_id=question_id).count()
    correct_answers = Answer.query.filter_by(question_id=question_id, is_correct=True).count()
    
    correct_rate = (correct_answers / total_answers * 100) if total_answers > 0 else 0

    option_distribution = {}
    if question.question_type == 'multiple_choice' and question.options:
        answers = Answer.query.filter_by(question_id=question_id).all()
        for answer in answers:
            option_distribution[answer.answer_text] = option_distribution.get(answer.answer_text, 0) + 1

    return {
        "question_id": question.id,
        "question_text": question.question_text,
        "total_answers": total_answers,
        "correct_answers": correct_answers,
        "correct_rate": f"{correct_rate:.2f}%",
        "option_distribution": option_distribution
    }

# Get Question Statistics (Speaker/Organizer) - Public API Endpoint
@quiz_bp.route('/questions/<int:question_id>/stats', methods=['GET'])
@jwt_required()
def get_question_stats(question_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"msg": "Question not found"}), 404
    
    presentation = Presentation.query.get(question.presentation_id)
    if not (user.role.name == 'organizer' or (user.role.name == 'speaker' and presentation.speaker_id == int(current_user_id))):
        return jsonify({"msg": "Unauthorized to view question statistics"}), 403

    stats_data = _get_question_stats_data(question_id)
    if stats_data is None:
        return jsonify({"msg": "Question not found"}), 404 # Should not happen if question is found above

    return jsonify(stats_data), 200

def _get_listener_report_data(presentation_id, user_id):
    """Helper function to get listener report data as a dictionary."""
    listener = User.query.get(user_id)
    # Log for debugging, keep this for now
    current_app.logger.info(f"Attempting to get report for user_id: {user_id}")
    if listener:
        current_app.logger.info(f"Found listener: {listener.username}, Role: {listener.role.name}")
    else:
        current_app.logger.warning(f"Listener with user_id {user_id} not found.")

    if not listener or listener.role.name != 'listener':
        current_app.logger.warning(f"User {user_id} is not a listener or not found.")
        return None # Indicate failure to get data

    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return None # Indicate failure

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

    return {
        "listener_id": listener.id,
        "listener_username": listener.username,
        "presentation_id": presentation.id,
        "presentation_title": presentation.title,
        "total_questions_in_presentation": total_questions,
        "answered_questions": answered_questions_count,
        "correct_answers": correct_answers_count,
        "accuracy_rate": f"{accuracy_rate:.2f}%",
        "question_details": question_details
    }

# Get Listener's Report for a Presentation (Listener/Organizer/Speaker) - Public API Endpoint
@quiz_bp.route('/presentations/<int:presentation_id>/report/<int:user_id>', methods=['GET'])
@jwt_required()
def get_listener_report(presentation_id, user_id):
    current_user_id = get_jwt_identity()
    requester = User.query.get(current_user_id)
    presentation = Presentation.query.get(presentation_id)
    
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404
    
    # 权限检查：
    # 1. 听众只能查看自己的报告
    # 2. 组织者可以查看任何听众的报告
    # 3. 演讲者可以查看与其演讲关联的听众报告
    is_authorized = (
        requester.role.name == 'organizer' or 
        (requester.role.name == 'listener' and requester.id == user_id) or
        (requester.role.name == 'speaker' and presentation.speaker_id == int(current_user_id))
    )
    
    if not is_authorized:
        return jsonify({"msg": "Unauthorized to view this report"}), 403

    report_data = _get_listener_report_data(presentation_id, user_id)
    if report_data is None:
        # This means either listener not found, or presentation not found, or not a listener role
        # The helper function returns None for these cases.
        # We need to differentiate the error messages.
        listener = User.query.get(user_id)
        if not listener or listener.role.name != 'listener':
            return jsonify({"msg": "User is not a listener"}), 404
        presentation = Presentation.query.get(presentation_id)
        if not presentation:
            return jsonify({"msg": "Presentation not found"}), 404
        return jsonify({"msg": "Could not retrieve report data"}), 500 # Generic error if other checks pass but data is None

    return jsonify(report_data), 200

# Get Overall Presentation Statistics (Organizer and Speaker)
@quiz_bp.route('/presentations/<int:presentation_id>/overall_stats', methods=['GET'])
@jwt_required() # 改为使用JWT验证，不再限制角色
def get_overall_presentation_stats(presentation_id):
    current_user_id = int(get_jwt_identity()) # 获取当前用户ID
    user = User.query.get(current_user_id)
    
    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404
    
    # 检查用户是否是organizer或者是该演讲的speaker
    if user.role.name != 'organizer' and presentation.speaker_id != current_user_id:
        return jsonify({"msg": "Unauthorized to view presentation statistics"}), 403

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
        listener_report = _get_listener_report_data(presentation_id, listener.id) # Call the helper function
        if listener_report: # Ensure report was retrieved successfully
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
    if file_record.user_id != int(current_user_id):
        # If file is linked to a presentation, check if speaker owns that presentation
        if file_record.presentation_id and file_record.presentation.speaker_id == int(current_user_id):
            pass # OK, speaker owns the presentation
        else:
            return jsonify({"msg": "Unauthorized to use this file"}), 403

    presentation = Presentation.query.get(presentation_id)
    if not presentation:
        return jsonify({"msg": "Presentation not found"}), 404
    if presentation.speaker_id != int(current_user_id):
        return jsonify({"msg": "You are not the speaker of this presentation"}), 403

    s3_client = current_app.config.get('S3_CLIENT')
    s3_bucket_name = current_app.config.get('S3_BUCKET_NAME')
    llm_api_url = current_app.config.get('LLM_API_URL')
    deepseek_api_key = current_app.config.get('DEEPSEEK_API_KEY')

    if not s3_client or not s3_bucket_name:
        return jsonify({"msg": "S3/R2 storage not configured"}), 500
    if not llm_api_url or not deepseek_api_key:
        return jsonify({"msg": "LLM API URL or Key not configured"}), 500

    try:
        # Initialize OpenAI client with DeepSeek base URL
        client = OpenAI(api_key=deepseek_api_key, base_url=llm_api_url)

        # Download file content from S3
        file_object = s3_client.get_object(Bucket=s3_bucket_name, Key=file_record.s3_key)
        file_content_bytes = file_object['Body'].read()

        # Use extracted_text_content from the database
        extracted_text = file_record.extracted_text_content
        if not extracted_text:
            return jsonify({"msg": "No extracted text content found for this file"}), 400

        # Step 1: Summarize the extracted text using LLM
        summary_system_prompt = "你是一个有用的助手，请对提供的文本进行精简总结，提取核心要点，用于后续生成测验题目。总结应简洁明了，保留关键信息。"
        summary_user_prompt = f"请总结以下文本：\n\n{extracted_text}"
        
        current_app.logger.info("Calling LLM API for summarization...")
        summary_response = client.chat.completions.create(
            model="deepseek-chat", # Specify the model
            messages=[
                {"role": "system", "content": summary_system_prompt},
                {"role": "user", "content": summary_user_prompt},
            ],
            stream=False
        )
        summarized_text = summary_response.choices[0].message.content

        current_app.logger.info(f"Summarized text length: {len(summarized_text)}")

        # Step 2: Generate questions based on the summarized text and user's prompt
        question_system_prompt = """你是一个专业的出题人，请根据提供的文本内容，生成高质量的单项选择题。
每个问题应具有深度，字数不少于60字。
每个选项的答案字数长度不少于20字。
请确保每个问题只有一个正确答案。
请严格以JSON数组的格式返回题目，每个题目对象包含 'question_text', 'question_type', 'options', 'correct_answer' 字段。
例如：
[
  {
    "question_text": "关于Python语言的特点，以下哪个描述是正确的？",
    "question_type": "multiple_choice",
    "options": ["Python是一种编译型语言，执行效率极高，不适合快速开发。", "Python是一种解释型语言，拥有丰富的第三方库，支持多种编程范式。", "Python主要用于系统级编程，对内存管理有严格要求，学习曲线陡峭。", "Python是一种强类型静态语言，变量类型在编译时确定，不具备动态特性。"],
    "correct_answer": "Python是一种解释型语言，拥有丰富的第三方库，支持多种编程范式。"
  }
]
"""
        question_user_prompt = f"请根据以下总结文本生成题目：\n\n{summarized_text}\n\n{prompt}"

        current_app.logger.info("Calling LLM API for question generation...")
        llm_response = client.chat.completions.create(
            model="deepseek-chat", # Specify the model
            messages=[
                {"role": "system", "content": question_system_prompt},
                {"role": "user", "content": question_user_prompt},
            ],
            stream=False
        )
        
        llm_raw_content = llm_response.choices[0].message.content
        current_app.logger.info(f"Raw LLM response content: {llm_raw_content}") # Log raw response for debugging

        # Attempt to parse the content as JSON
        try:
            # Clean up potential markdown code blocks if LLM wraps JSON in them
            if llm_raw_content.startswith("```json") and llm_raw_content.endswith("```"):
                json_string = llm_raw_content[len("```json"):-len("```")].strip()
            else:
                json_string = llm_raw_content.strip()
            
            generated_questions_data = json.loads(json_string)
        except json.JSONDecodeError as e:
            current_app.logger.error(f"Failed to parse LLM response as JSON: {e}. Raw response: {llm_raw_content}")
            return jsonify({"msg": f"Failed to parse LLM response: {str(e)}. Raw response might not be valid JSON."}), 500

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
                is_active=True # 设置为活跃状态，这样生成后可以立即使用
            )
            db.session.add(new_question) # Move inside the loop
            new_questions.append(new_question) # Move inside the loop

        db.session.commit()

        # 注释WebSocket相关代码 - 暂时不使用实时广播功能
        # # 为每个生成的问题发送Socket.IO通知
        # for question in new_questions:
        #     question_data = {
        #         "id": question.id,
        #         "question_text": question.question_text,
        #         "question_type": question.question_type,
        #         "options": json.loads(question.options) if question.options else None,
        #         "is_active": True  # 确保通知中也标记为活跃状态
        #     }
        #     socketio.emit('new_question', question_data, room=f'presentation_{presentation_id}')

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
