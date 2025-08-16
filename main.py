from app import create_app
from app.extensions import socket # Import the socketio instance

# Create the Flask app instance using your factory
app = create_app()

# The main entry point for the application
if __name__ == '__main__':
    # Use socket.run() to start the development server.
    # This will use a server that supports WebSockets, like eventlet.
    socket.run(app, debug=True, port=5000, host="0.0.0.0")