import os
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import models
from celery import Celery
from routers import auth, goals, habits, initiatives, social
from ws import ws_router
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse

# --- Environment & Setup ---
DATABASE_PATH = os.environ.get("DATABASE_PATH", "goals.db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.init_db(DATABASE_PATH)
    yield
    pass


app = FastAPI(title="One-Minute Manager API", lifespan=lifespan)


# Setup Celery
def make_celery():
    celery_app = Celery(
        "tasks", broker=os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    )
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
    )
    return celery_app


celery = make_celery()

app.include_router(auth.router)
app.include_router(goals.router)
app.include_router(habits.router)
app.include_router(initiatives.router)
app.include_router(social.router)
app.include_router(ws_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers for consistency with Flask
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    print(f"Exception: {exc}")
    return JSONResponse(
        status_code=500, content={"error": "An internal server error occurred."}
    )


@app.post("/sms")
async def sms_reply(Body: str = Form(None)):
    resp = MessagingResponse()
    body = Body.strip().lower() if Body else ""

    if body == "list":
        goals = models.list_pending_goals(user_id=1)
        if not goals:
            resp.message("No pending daily goals. Great job!")
        else:
            msg = "Pending Goals:\\n"
            for g in goals:
                msg += f"[{g['id']}] {g['description']}\\n"
                for sub in g.get("subgoals", []):
                    msg += f"- [{sub['id']}] {sub['description']}\\n"
            resp.message(msg)
    elif body.startswith("complete"):
        parts = body.split(" ")
        if len(parts) > 1 and parts[1].isdigit():
            goal_id = int(parts[1])
            success = models.complete_goal(goal_id, user_id=1)
            if success:
                resp.message(f"Goal {goal_id} marked as completed.")
            else:
                resp.message(f"Goal {goal_id} not found.")
        else:
            resp.message("Send 'complete <id>' to mark a goal as done.")
    else:
        resp.message(
            "Welcome to One-Minute Manager. Reply 'list' to see pending goals."
        )

    return Response(content=str(resp), media_type="application/xml")


@app.post("/voice")
async def voice_reply():
    resp = VoiceResponse()
    resp.say("Hello. I am your One-Minute Manager. You are doing great today. Goodbye.")
    return Response(content=str(resp), media_type="application/xml")


# Static files / Vue fallback
if os.path.exists("dist"):
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")


@app.get("/{full_path:path}")
async def serve_vue(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not Found")

    if os.path.exists("dist/index.html"):
        return FileResponse("dist/index.html")
    else:
        return JSONResponse(
            {"error": "Frontend not built. Run 'npm run build' in frontend directory."}
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
