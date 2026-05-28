from fastapi import APIRouter, Depends, HTTPException
from auth_utils import get_current_user
import models
import schemas
from tasks import breakdown_goal_task

router = APIRouter(prefix="/api/goals")


@router.get("")
def get_goals(current_user: models.User = Depends(get_current_user)):
    goals = models.list_pending_goals(user_id=current_user.id)
    return {"goals": goals}


@router.post("", status_code=201)
def add_goal(
    goal_data: schemas.GoalCreate, current_user: models.User = Depends(get_current_user)
):
    goal = models.add_goal(
        goal_data.description, user_id=current_user.id, parent_id=goal_data.parent_id
    )
    return {"message": "Goal added.", "goal": goal}


@router.post("/{goal_id}/complete")
def complete_goal(goal_id: int, current_user: models.User = Depends(get_current_user)):
    success = models.complete_goal(goal_id, user_id=current_user.id)
    if success:
        return {"message": f"Goal {goal_id} completed."}
    raise HTTPException(status_code=404, detail="Goal not found.")


@router.delete("/{goal_id}")
def delete_goal(goal_id: int, current_user: models.User = Depends(get_current_user)):
    success = models.delete_goal(goal_id, user_id=current_user.id)
    if success:
        return {"message": f"Goal {goal_id} deleted."}
    raise HTTPException(status_code=404, detail="Goal not found.")


@router.get("/completed")
def get_completed_goals(current_user: models.User = Depends(get_current_user)):
    goals = models.list_completed_goals(user_id=current_user.id)
    return {"goals": goals}


@router.get("/calendar")
def get_calendar_goals(current_user: models.User = Depends(get_current_user)):
    calendar = models.list_calendar_goals(user_id=current_user.id)
    return {"calendar": calendar}


@router.post("/breakdown")
def breakdown_goal(
    request: schemas.GoalBreakdownRequest,
    current_user: models.User = Depends(get_current_user),
):
    subgoals = breakdown_goal_task(request.description, current_user.id)
    return {"subgoals": subgoals}
