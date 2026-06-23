import extensions
from fastapi import APIRouter, Depends, HTTPException
import models
from routers.auth_deps import get_current_user

router = APIRouter(prefix="/api/social")


@router.get("/users")
def get_public_users(user=Depends(get_current_user)):
    users = models.list_public_users()
    return users


@router.get("/users/{user_id}/profile")
def get_user_profile(user_id: int, user=Depends(get_current_user)):
    target_user = models.get_user_by_id(user_id)
    if not target_user or getattr(target_user, "is_public", False) is False:
        raise HTTPException(status_code=404, detail="User not found or is private")

    recent_completed = models.list_completed_goals(user_id=target_user.id)
    recent_completed = recent_completed[:10]

    return {
        "id": target_user.id,
        "username": target_user.username,
        "avatar_url": getattr(target_user, "avatar_url", None),
        "recent_completed_goals": recent_completed,
    }


@router.post("/goals/{goal_id}/highfive")
def api_high_five(goal_id: int, user=Depends(get_current_user)):
    # In a real app we might check if the goal belongs to a public user
    success = models.add_high_five(goal_id, user.id)
    if success:
        # Get target user to notify them dynamically
        with models.session_scope() as session:
            g = session.get(models.Goal, goal_id)
            if g and g.user_id != user.id:
                extensions.sync_emit(
                    "high_five_received",
                    {"goal_id": goal_id, "from": user.username},
                    to=str(g.user_id),
                )
        return {"message": "High-five sent!"}
    raise HTTPException(status_code=404, detail="Goal not found")


@router.get("/leaderboard")
def api_leaderboard(user=Depends(get_current_user)):
    board = models.get_leaderboard()
    return board
