from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create database object
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # ✅ REQUIRED for session, login, flash
    app.config['SECRET_KEY'] = 'your-secret-key'

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ Correct way to initialize db
    db.init_app(app)

    # Import blueprints
    from app.routes.auth import auth_bp
    from app.routes.task import task_bp   # <-- filename must be tasks.py

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app
