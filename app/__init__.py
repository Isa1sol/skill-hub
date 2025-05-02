import os
from flask import Flask
from app.extensions import db, login_manager, socketio
from app.routes import bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config['SECRET_KEY'] = 'your-secret-key'
    os.makedirs(app.instance_path, exist_ok=True)

    # SQLite database file stored in instance/ directory
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path,'skillhub.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    app.register_blueprint(bp)

    return app
