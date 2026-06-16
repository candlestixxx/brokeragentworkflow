import asyncio
import socketio

# Initialize the python-socketio AsyncServer
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

# Create an ASGI app to wrap the socket.io server
socket_app = socketio.ASGIApp(sio)

# Keep a reference to socketio for backwards compatibility in other modules if needed
# though we'll update them to use `sio` directly.
socketio_server = sio

def sync_emit(event, data, to=None):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        loop.create_task(sio.emit(event, data, to=to))
    else:
        asyncio.run(sio.emit(event, data, to=to))
