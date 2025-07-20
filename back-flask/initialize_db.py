import os
from app import create_app
from app.models import db, Role, User, Presentation, Question, Answer, Feedback, DiscussionComment, File # Import db and all models

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app, _ = create_app() # Get the app instance

with app.app_context():
    # Remove existing database file if it exists
    if os.path.exists('site.db'):
        os.remove('site.db')
        print("Removed existing site.db for a clean start.")

    db.metadata.create_all(db.engine) # Use db.metadata.create_all with db.engine
    db.session.commit() # Add commit here
    print("Database tables created.")

    # Verify table creation
    try:
        result = db.engine.execute("PRAGMA table_info(role);").fetchall()
        if result:
            print("Role table exists and has columns.")
        else:
            print("Role table does not exist or has no columns after creation.")
    except Exception as e:
        print(f"Error verifying role table: {e}")

    db.session.close() # Close the session to ensure fresh state
    db.session.begin() # Start a new session

    # Initialize roles if they don't exist
    if not Role.query.filter_by(name='organizer').first():
        db.session.add(Role(name='organizer'))
    if not Role.query.filter_by(name='speaker').first():
        db.session.add(Role(name='speaker'))
    if not Role.query.filter_by(name='listener').first():
        db.session.add(Role(name='listener'))
    db.session.commit()
    print("Roles initialized.")

print("Database initialization complete.")
