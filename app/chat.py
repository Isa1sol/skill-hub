from app import socketio
from flask_socketio import send

@socketio.on('message')
def handle_message(data):
    send(data, broadcast=True)
