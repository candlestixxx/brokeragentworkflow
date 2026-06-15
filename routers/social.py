from fastapi import APIRouter, Depends, HTTPException, status
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
    if not target_user or getattr(target_user, 'is_public', False) == False:
        raise HTTPException(status_code=404, detail="User not found or is private")

    recent_completed = models.list_completed_goals(user_id=target_user.id)
    recent_completed = recent_completed[:10]

    return {
        "id": target_user.id,
        "username": target_user.username,
        "avatar_url": getattr(target_user, 'avatar_url', None),
        "recent_completed_goals": recent_completed
    }
