from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import models
from extensions import socket_app

from routers import auth, goals, habits, social, analytics, initiatives, webhooks

app = FastAPI()

# Mount Socket.IO app
app.mount("/socket.io", socket_app)

# Ensure DB is initialized before first request
@app.on_event("startup")
def startup_event():
    models.init_db()

# Register Routers
app.include_router(auth.router)
app.include_router(goals.router)
app.include_router(habits.router)
app.include_router(social.router)
app.include_router(analytics.router)
app.include_router(initiatives.router)
app.include_router(webhooks.router)

# Mount static files (Vue dist)
dist_dir = os.path.join(os.path.dirname(__file__), "dist")
if os.path.exists(dist_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(dist_dir, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_vue_app(full_path: str):
        # Serve the index.html for any route not matched by API to let Vue handle routing
        if not full_path.startswith("api/") and not full_path.startswith("socket.io/"):
            index_file = os.path.join(dist_dir, "index.html")
            if os.path.exists(index_file):
                return FileResponse(index_file)
        # We can handle 404s properly later if needed.
        return {"detail": "Not Found"}
else:
    print(f"Warning: dist directory not found at {dist_dir}. Vue app won't be served.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
