import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Secret key for sessions
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")

# Database config (uses SQLite by default, PostgreSQL in production)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///skillhub.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Use eventlet in production
CORS(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"  # Optional: redirects to login page if not logged in
login_manager.init_app(app)

# Import routes and other blueprints/modules
from app import routes, models, chat, ai
