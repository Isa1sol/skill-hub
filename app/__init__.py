import os
from flask import Flask
from app.extensions import db, login_manager, socketio
from app.routes import bp
from flask_migrate import Migrate  # Import Migrate
from .models import User
from app.auth import auth_bp
from app.main import main_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
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

    migrate = Migrate(app, db)  # Initialize Migrate
    app.register_blueprint(bp)

    return app
