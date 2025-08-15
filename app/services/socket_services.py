from flask_socketio import emit, join_room
from app.extensions import socket

@socket.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {'data': 'Welcome to the quiz!'})
    
    
@socket.on("join")
def handle_joni(data):
    room = data["room"]
    join_room(room)
    emit('message', {'data': f"{data['username']} joined {room}"}, to=room)

@socket.on("ready")
def handle_ready(data):
    room = data["room"]
    join_room(room)
    emit('message', {'data': f"{data['username']} is ready on room -> {room}"}, to=room)
    