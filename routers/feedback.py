import extensions
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import models
from routers.auth_deps import get_current_user
from notifications import notify_all

router = APIRouter(prefix="/api/feedback")

class FeedbackRequest(BaseModel):
    receiver_id: int
    message: str
    feedback_type: str

@router.post("", status_code=201)
def api_add_feedback(data: FeedbackRequest, user=Depends(get_current_user)):
    if not data.message or not data.feedback_type:
         raise HTTPException(status_code=400, detail="Message and feedback_type required.")
    if data.feedback_type not in ["praise", "redirect"]:
         raise HTTPException(status_code=400, detail="Invalid feedback type.")

    models.add_feedback(user.id, data.receiver_id, data.message, data.feedback_type)

    notify_all(
        subject="New Feedback Received",
        body=f"You received a new {data.feedback_type} from {user.username}.",
        speakable_message=f"You received a new {data.feedback_type} from {user.username}.",
    )
    extensions.sync_emit(
        "data_updated", {"message": f"New {data.feedback_type} received"}, to=str(data.receiver_id)
    )

    return {"message": "Feedback sent."}

@router.get("")
def api_get_feedback(user=Depends(get_current_user)):
    feedback = models.get_user_feedback(user.id)
    return {"feedback": feedback}
