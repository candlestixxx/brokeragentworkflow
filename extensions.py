# Allow importing the global socketio instance
from flask_socketio import SocketIO

# We initialize it here without an app, and init_app later in app.py
socketio = SocketIO(cors_allowed_origins="*")
