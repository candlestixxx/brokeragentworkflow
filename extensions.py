import logging
import asyncio
import socketio

# Initialize the python-socketio AsyncServer
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

# Create an ASGI app to wrap the socket.io server
socket_app = socketio.ASGIApp(sio)

# Keep a reference to socketio for backwards compatibility in other modules if needed
# though we'll update them to use `sio` directly.
socketio_server = sio


# We need to bridge the async emit into the running loop safely from a sync thread


_main_loop = None


def get_main_loop():
    global _main_loop
    return _main_loop


def set_main_loop(loop):
    global _main_loop
    _main_loop = loop


def sync_emit(event, data, to=None):
    loop = get_main_loop()
    if loop and loop.is_running():
        # Dispatch to the main event loop thread safely
        asyncio.run_coroutine_threadsafe(sio.emit(event, data, to=to), loop)
    else:
        logging.warning("No main event loop running, skipping sync_emit")
