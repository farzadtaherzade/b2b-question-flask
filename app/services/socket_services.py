from flask_socketio import emit, join_room
from app.extensions import socket
from app.models.player import Player
from app.extensions import db

@socket.on('connect')
def on_client_connect():
    emit('welcome_message', {'data': 'Welcome to the quiz!'}, callback=lambda: print("Welcome message sent"))

@socket.on('join')
def on_room_join(data):
    try:
        room_id = data['room']
        username = data['username']
        join_room(room_id)
        emit('room_joined', {'data': f"{username} joined {room_id}"}, to=room_id)
    except Exception as e:
        emit('error', {'data': f"Join error: {str(e)}"})
        raise

@socket.on('ready')
def on_player_ready(data):
    room_id = data['room']
    username = data['username']
    player = Player.query.filter_by(username=username, session_id=room_id).first()
    if player is None:
        emit('error', {'data': f"Player '{username}' not found in room '{room_id}'"})
        return
    player.is_ready = True
    db.session.add(player)
    db.session.commit()
    join_room(room_id)
    emit('status_message', {'data': f"{username} is ready in room {room_id}"}, to=room_id)

@socket.on('chat_message')
def on_chat_message(data):
    room_id = data.get('room')
    username = data.get('username')
    text = data.get('text')
    if not all([room_id, username, text]):
        emit('error', {'data': 'Missing room, username, or message'})
        return
    emit('chat_message_received', {'sender': username, 'text': text}, to=room_id)