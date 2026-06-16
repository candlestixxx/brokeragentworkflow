import socketio

# Initialize the python-socketio AsyncServer
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

# Create an ASGI app to wrap the socket.io server
socket_app = socketio.ASGIApp(sio)

# Keep a reference to socketio for backwards compatibility in other modules if needed
# though we'll update them to use `sio` directly.
socketio_server = sio
