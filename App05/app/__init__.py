from flask import Flask
try:
    from flask_sqlalchemy import SQLAlchemy
except ImportError:
    raise ImportError("flask-sqlalchemy is not installed. Install it using: pip install flask-sqlalchemy")

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET-KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqllite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.__init__(app)

    from app.routes.auth import auth_bp
    from app.routes.auth import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app