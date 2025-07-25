from flask_sqlalchemy import SQLAlchemy
import datetime # Add this import

db = SQLAlchemy()

user_presentations = db.Table('user_presentations',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('presentation_id', db.Integer, db.ForeignKey('presentation.id'), primary_key=True)
)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False) # e.g., 'organizer', 'speaker', 'listener'
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f"Role('{self.name}')"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    # For speakers
    presentations_as_speaker = db.relationship('Presentation', backref='speaker', lazy=True, foreign_keys='Presentation.speaker_id')
    # For listeners
    presentations_as_listener = db.relationship('Presentation', secondary=user_presentations, backref=db.backref('listeners', lazy='dynamic'))

    def __repr__(self):
        return f"User('{self.username}', Role: '{self.role.name}')"

class Presentation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    speaker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Speaker is a User

    def __repr__(self):
        return f"Presentation('{self.title}', Speaker: '{self.speaker.username}')"

# New models for Task 2
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    presentation_id = db.Column(db.Integer, db.ForeignKey('presentation.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False, default='multiple_choice') # e.g., 'multiple_choice', 'true_false'
    options = db.Column(db.Text, nullable=True) # JSON string of options
    correct_answer = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True) # Whether the question is currently open for answers

    presentation = db.relationship('Presentation', backref=db.backref('questions', lazy=True))

    def __repr__(self):
        return f"Question('{self.question_text}')"

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=True) # Null until graded

    question = db.relationship('Question', backref=db.backref('answers', lazy=True))
    user = db.relationship('User', backref=db.backref('answers', lazy=True))

    def __repr__(self):
        return f"Answer(User:{self.user_id}, Question:{self.question_id}, Answer:'{self.answer_text}')"

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    presentation_id = db.Column(db.Integer, db.ForeignKey('presentation.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback_type = db.Column(db.String(100), nullable=False) # e.g., 'too_fast', 'too_slow', 'boring', 'bad_question'
    content = db.Column(db.Text, nullable=True) # 添加反馈内容字段，可选
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    presentation = db.relationship('Presentation', backref=db.backref('feedbacks', lazy=True))
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))

    def __repr__(self):
        return f"Feedback(Type:'{self.feedback_type}', Presentation:{self.presentation_id})"

class DiscussionComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('discussion_comment.id'), nullable=True)

    question = db.relationship('Question', backref=db.backref('comments', lazy=True))
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    replies = db.relationship('DiscussionComment', backref=db.backref('parent', remote_side=[id]), lazy=True)

    def __repr__(self):
        return f"Comment(User:{self.user_id}, Question:{self.question_id}, Comment:'{self.comment_text}')"

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    s3_key = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    presentation_id = db.Column(db.Integer, db.ForeignKey('presentation.id'), nullable=True) # Optional: link to a presentation
    upload_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    file_type = db.Column(db.String(100), nullable=True)
    size = db.Column(db.BigInteger, nullable=True) # Size in bytes
    extracted_text_content = db.Column(db.Text, nullable=True) # New field to store extracted text

    user = db.relationship('User', backref=db.backref('uploaded_files', lazy=True))
    presentation = db.relationship('Presentation', backref=db.backref('files', lazy=True))

    def __repr__(self):
        return f"File('{self.filename}', S3 Key: '{self.s3_key}')"
