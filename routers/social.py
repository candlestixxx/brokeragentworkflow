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

    recent_completed = models.list_completed_goals(user_id=target_user['id'])
    recent_completed = recent_completed[:10]

    return {
        "id": target_user['id'],
        "username": target_user['username'],
        "avatar_url": getattr(target_user, "avatar_url", None),
        "recent_completed_goals": recent_completed,
    }


@router.get("/leaderboard")
def get_leaderboard(user=Depends(get_current_user)):
    users = models.list_public_users()
    leaderboard = []
    for u in users:
        completed = models.list_completed_goals(user_id=u['id'])
        leaderboard.append(
            {"id": u['id'], "username": u['username'], "score": len(completed)}
        )
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    return leaderboard[:10]


@router.post("/goals/{goal_id}/highfive")
def highfive_goal(goal_id: int, user=Depends(get_current_user)):
    success = models.add_high_five(goal_id=goal_id, sender_id=user['id'])
    if not success:
        raise HTTPException(status_code=400, detail="Could not add high five")

    import extensions

    extensions.sync_emit(
        "high_five_received", {"goal_id": goal_id, "sender": user['username']}
    )

    return {"message": "High five added!"}
