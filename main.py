from flask import Flask
from app.extensions import db, login_manager, socketio
from app.routes import bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'

    # Use DATABASE_URL from Render's environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    app.register_blueprint(bp)

    # Create tables automatically if they don't exist
    with app.app_context():
        from app import models
        db.create_all()

    return app
