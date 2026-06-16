import extensions
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from notifications import notify_all
import models
from extensions import socketio_server, sync_emit
from routers.auth_deps import get_current_user

router = APIRouter(prefix="/api/goals")


class GoalRequest(BaseModel):
    description: str | None = None
    parent_id: int | None = None


class BreakdownRequest(BaseModel):
    description: str | None = None


@router.get("")
def api_get_goals(user=Depends(get_current_user)):
    goals = models.list_pending_goals(user_id=user.id)
    return {"goals": goals}


@router.get("/completed")
def api_get_completed_goals(user=Depends(get_current_user)):
    goals = models.list_completed_goals(user_id=user.id)
    return {"goals": goals}


@router.get("/calendar")
def api_get_calendar_goals(user=Depends(get_current_user)):
    calendar_data = models.list_calendar_goals(user_id=user.id)
    return {"calendar": calendar_data}


@router.post("", status_code=201)
def api_add_goal(data: GoalRequest, user=Depends(get_current_user)):
    if data.description:
        goal_data = models.add_goal(
            data.description, user_id=user.id, parent_id=data.parent_id
        )
        notify_all(
            subject="New Goal Added",
            body=f"You added a new goal: {data.description}",
            speakable_message=f"You added a new goal: {data.description}",
        )
        extensions.sync_emit("goal_added", {"goal": goal_data}, to=str(user.id))
        return {"message": "Goal added.", "id": goal_data["id"]}
    raise HTTPException(status_code=400, detail="Description required.")


@router.post("/{goal_id}/complete")
def api_complete_goal(goal_id: int, user=Depends(get_current_user)):
    success = models.complete_goal(goal_id, user_id=user.id)
    if success:
        new_badges = models.evaluate_badges(user.id)

        notify_all(
            subject="Goal Completed!",
            body=f"Excellent work! You completed goal {goal_id}.",
            speakable_message=f"Excellent work! You completed goal {goal_id}.",
        )

        extensions.sync_emit("goal_completed", {"id": goal_id}, to=str(user.id))
        extensions.sync_emit(
            "data_updated", {"message": "Goal completed"}, to=str(user.id)
        )

        for badge in new_badges:
            extensions.sync_emit(
                "badge_awarded",
                {"name": badge["name"], "icon": badge["icon"]},
                to=str(user.id),
            )

        return {"message": f"Goal {goal_id} completed."}
    raise HTTPException(status_code=404, detail="Goal not found.")


@router.delete("/{goal_id}")
def api_delete_goal(goal_id: int, user=Depends(get_current_user)):
    success = models.delete_goal(goal_id, user_id=user.id)
    if success:
        extensions.sync_emit("goal_deleted", {"id": goal_id}, to=str(user.id))
        return {"message": f"Goal {goal_id} deleted."}
    raise HTTPException(status_code=404, detail="Goal not found.")


@router.post("/{goal_id}/breakdown")
def api_breakdown_goal(goal_id: int, user=Depends(get_current_user)):
    db_user = models.get_user_by_id(user.id)
    goal = db_user.goals

    target_goal = None
    for g in goal:
        if g.id == goal_id:
            target_goal = g
            break

    if not target_goal:
        raise HTTPException(status_code=404, detail="Goal not found.")

    description = target_goal.description

    sub_goals = [
        f"Research best approaches for: {description[:20]}...",
        f"Draft initial outline for: {description[:20]}...",
        f"Execute and review first steps of: {description[:20]}...",
    ]

    for sub_desc in sub_goals:
        models.add_goal(sub_desc, user_id=user.id, parent_id=goal_id)

    return {"subgoals": sub_goals}


@router.post("/breakdown")
def api_breakdown_goal_legacy(data: BreakdownRequest, user=Depends(get_current_user)):
    if not data.description:
        raise HTTPException(status_code=400, detail="Description required.")

    sub_goals = [
        f"Research best approaches for: {data.description[:20]}...",
        f"Draft initial outline for: {data.description[:20]}...",
        f"Execute and review first steps of: {data.description[:20]}...",
    ]

    return {"subgoals": sub_goals}
