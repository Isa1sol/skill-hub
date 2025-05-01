import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///skillhub.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Extensions
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Flask-Login Manager setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Optional: Redirect to 'login' if not authenticated
login_manager.init_app(app)

# Import routes, models, and other modules after app is created
from app import routes, models, chat, ai
