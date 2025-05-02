from flask import Flask
from app.extensions import db, login_manager, socketio
from app.routes import bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
    
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    app.register_blueprint(bp)

    return app
