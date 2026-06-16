from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from notifications import notify_all
import models
from extensions import socketio_server
from routers.auth_deps import get_current_user

router = APIRouter(prefix="/api/initiatives")


class InitiativeRequest(BaseModel):
    quarter: str | None = None
    description: str | None = None


@router.get("")
def api_get_initiatives(user=Depends(get_current_user)):
    initiatives = models.list_pending_initiatives(user_id=user.id)
    return {
        "initiatives": [
            {"id": i[0], "quarter": i[1], "description": i[2]} for i in initiatives
        ]
    }


@router.post("", status_code=201)
async def api_add_initiative(data: InitiativeRequest, user=Depends(get_current_user)):
    if data.quarter and data.description:
        init_id = models.add_initiative(data.quarter, data.description, user_id=user.id)
        notify_all(
            subject="New Initiative Added",
            body=f"You added a new initiative for {data.quarter}: {data.description}",
            speakable_message=f"You added a new quarterly initiative for {data.quarter}: {data.description}",
        )
        await socketio_server.emit(
            "data_updated", {"message": "Initiative added"}, to=str(user.id)
        )
        return {"message": "Initiative added.", "id": init_id}
    raise HTTPException(status_code=400, detail="Quarter and description required.")


@router.post("/{initiative_id}/complete")
async def api_complete_initiative(initiative_id: int, user=Depends(get_current_user)):
    success = models.complete_initiative(initiative_id, user_id=user.id)
    if success:
        notify_all(
            subject="Initiative Completed!",
            body=f"Great job completing quarterly initiative {initiative_id}.",
            speakable_message=f"Great job completing quarterly initiative {initiative_id}.",
        )
        await socketio_server.emit(
            "data_updated", {"message": "Initiative completed"}, to=str(user.id)
        )
        return {"message": f"Initiative {initiative_id} completed."}
    raise HTTPException(status_code=404, detail="Initiative not found.")
