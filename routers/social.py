from fastapi import APIRouter, Depends, HTTPException
from auth_utils import get_current_user
import models

router = APIRouter(prefix="/api/social")


@router.get("/users")
def get_public_users(current_user: models.User = Depends(get_current_user)):
    users = models.list_public_users()
    return users


@router.get("/users/{user_id}/profile")
def get_user_profile(
    user_id: int, current_user: models.User = Depends(get_current_user)
):
    user = models.get_user_by_id(user_id)
    if not user or not user.is_public:
        raise HTTPException(status_code=404, detail="User not found or is private")

    recent_completed = models.list_completed_goals(user_id=user.id)
    recent_completed = recent_completed[:10]

    badges = models.get_user_badges(user.id)

    return {
        "id": user.id,
        "username": user.username,
        "avatar_url": user.avatar_url,
        "recent_completed_goals": recent_completed,
        "badges": badges,
    }
