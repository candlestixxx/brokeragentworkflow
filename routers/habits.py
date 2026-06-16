from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import models
from extensions import socketio_server
from routers.auth_deps import get_current_user
from datetime import datetime

router = APIRouter(prefix="/api/habits")


class HabitRequest(BaseModel):
    description: str | None = None


@router.get("")
def api_get_habits(user=Depends(get_current_user)):
    habits = models.list_habits(user_id=user.id)
    return {"habits": habits}


@router.post("", status_code=201)
async def api_add_habit(data: HabitRequest, user=Depends(get_current_user)):
    if data.description:
        habit_id = models.add_habit(data.description, user_id=user.id)
        await socketio_server.emit(
            "data_updated", {"message": "Habit added"}, to=str(user.id)
        )
        return {"message": "Habit added.", "id": habit_id}
    raise HTTPException(status_code=400, detail="Description required.")


@router.post("/{habit_id}/complete")
async def api_complete_habit(habit_id: int, user=Depends(get_current_user)):
    today = datetime.now().strftime("%Y-%m-%d")
    success = models.complete_habit(habit_id, today, user_id=user.id)
    if success:
        await socketio_server.emit(
            "data_updated", {"message": "Habit completed"}, to=str(user.id)
        )
        return {"message": f"Habit {habit_id} completed for today."}
    raise HTTPException(
        status_code=400, detail="Habit not found or already completed today."
    )


@router.delete("/{habit_id}")
async def api_delete_habit(habit_id: int, user=Depends(get_current_user)):
    success = models.delete_habit(habit_id, user_id=user.id)
    if success:
        await socketio_server.emit(
            "data_updated", {"message": "Habit deleted"}, to=str(user.id)
        )
        return {"message": f"Habit {habit_id} deleted."}
    raise HTTPException(status_code=404, detail="Habit not found.")
