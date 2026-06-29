import socketio
from extensions import sio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import models

from routers import auth, goals, habits, social, analytics, initiatives, webhooks, coach

fastapi_app = FastAPI()
app = fastapi_app

# Mount Socket.IO app
# Wrapped by ASGIApp below


# Ensure DB is initialized before first request
@fastapi_app.on_event("startup")
def startup_event():
    import asyncio
    import extensions

    extensions.set_main_loop(asyncio.get_running_loop())
    models.init_db()


# Register Routers
fastapi_app.include_router(auth.router)
fastapi_app.include_router(goals.router)
fastapi_app.include_router(habits.router)
fastapi_app.include_router(social.router)
fastapi_app.include_router(analytics.router)
fastapi_app.include_router(initiatives.router)
fastapi_app.include_router(webhooks.router)
fastapi_app.include_router(coach.router)

# Mount static files (Vue dist)
dist_dir = os.path.join(os.path.dirname(__file__), "dist")
if os.path.exists(dist_dir):
    app.mount(
        "/assets",
        StaticFiles(directory=os.path.join(dist_dir, "assets")),
        name="assets",
    )

    @fastapi_app.get("/{full_path:path}")
    async def serve_vue_app(full_path: str):
        if not full_path.startswith("api/") and not full_path.startswith("socket.io/"):
            # Check if it's a direct file request (e.g. favicon.ico, vite.svg)
            potential_file = os.path.join(dist_dir, full_path)
            if os.path.exists(potential_file) and os.path.isfile(potential_file):
                return FileResponse(potential_file)

            index_file = os.path.join(dist_dir, "index.html")
            if os.path.exists(index_file):
                return FileResponse(index_file)
        return {"detail": "Not Found"}
else:
    print(f"Warning: dist directory not found at {dist_dir}. Vue app won't be served.")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)

app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app, socketio_path="socket.io")
