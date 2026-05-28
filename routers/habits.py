from fastapi import APIRouter, Depends, HTTPException
from auth_utils import get_current_user
import models
import schemas
from datetime import datetime

router = APIRouter(prefix="/api/habits")


@router.get("")
def get_habits(current_user: models.User = Depends(get_current_user)):
    habits = models.list_habits(user_id=current_user.id)
    return {"habits": habits}


@router.post("", status_code=201)
def add_habit(
    habit_data: schemas.HabitCreate,
    current_user: models.User = Depends(get_current_user),
):
    habit_id = models.add_habit(habit_data.description, user_id=current_user.id)
    return {"message": "Habit added.", "id": habit_id}


@router.post("/{habit_id}/complete")
def complete_habit(
    habit_id: int, current_user: models.User = Depends(get_current_user)
):
    today_str = datetime.now().strftime("%Y-%m-%d")
    success = models.complete_habit(habit_id, today_str, user_id=current_user.id)
    if success:
        return {"message": f"Habit {habit_id} completed for today."}
    raise HTTPException(
        status_code=404, detail="Habit not found or could not be updated."
    )


@router.delete("/{habit_id}")
def delete_habit(habit_id: int, current_user: models.User = Depends(get_current_user)):
    success = models.delete_habit(habit_id, user_id=current_user.id)
    if success:
        return {"message": f"Habit {habit_id} deleted."}
    raise HTTPException(status_code=404, detail="Habit not found.")
