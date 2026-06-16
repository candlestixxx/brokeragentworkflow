from fastapi import APIRouter, Depends, HTTPException, Response, Request
from pydantic import BaseModel
import models
from routers.auth_deps import manager, get_current_user, get_current_user_optional

router = APIRouter(prefix="/api")


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


class SettingsRequest(BaseModel):
    notifications_enabled: bool | None = None
    is_public: bool | None = None


class AvatarRequest(BaseModel):
    avatar_url: str


@router.get("/me/analytics")
def api_me_analytics(user=Depends(get_current_user)):
    completed_goals = len(models.list_completed_goals(user_id=user.id))
    active_initiatives = len(models.list_pending_initiatives(user_id=user.id))
    habits = models.list_habits(user_id=user.id)
    total_habits = len(habits)
    longest_streak = max([h["highest_streak"] for h in habits]) if habits else 0

    return {
        "completed_goals": completed_goals,
        "active_initiatives": active_initiatives,
        "total_habits": total_habits,
        "longest_streak": longest_streak,
    }


@router.get("/me")
def api_me(request: Request):
    token = request.cookies.get("session")
    user = None
    if token:
        try:
            user = get_current_user_optional(request)
        except Exception:
            pass

    if user:
        return {
            "authenticated": True,
            "user_id": user.id,
            "username": user.username,
            "avatar_url": user.avatar_url,
            "notifications_enabled": user.notifications_enabled,
            "is_public": getattr(user, "is_public", False),
            "has_completed_onboarding": getattr(
                user, "has_completed_onboarding", False
            ),
            "badges": models.get_user_badges(user.id),
        }
    return {"authenticated": False}


@router.post("/me/onboarding")
def api_complete_onboarding(user=Depends(get_current_user)):
    with models.session_scope() as session:
        db_user = session.get(models.User, user.id)
        if db_user:
            db_user.has_completed_onboarding = True
            return {"message": "Onboarding completed."}
    raise HTTPException(status_code=500, detail="Update failed.")


@router.post("/me/settings")
def api_update_settings(data: SettingsRequest, user=Depends(get_current_user)):
    if data.notifications_enabled is None and data.is_public is None:
        raise HTTPException(status_code=400, detail="Missing setting parameters.")

    notif_val = data.notifications_enabled
    pub_val = data.is_public

    success = models.update_user_settings(user.id, notif_val, pub_val)
    if success:
        return {"message": "Settings updated."}
    raise HTTPException(status_code=500, detail="Update failed.")


@router.post("/me/avatar")
def api_update_avatar(data: AvatarRequest, user=Depends(get_current_user)):
    if not data.avatar_url:
        raise HTTPException(status_code=400, detail="Avatar URL required.")

    success = models.update_user_avatar(user.id, data.avatar_url)
    if success:
        return {"message": "Avatar updated."}
    raise HTTPException(status_code=500, detail="Update failed.")


@router.post("/login")
def api_login(data: LoginRequest, response: Response):
    user = models.get_user_by_username(data.username)
    if user and user.check_password(data.password):
        access_token = manager.create_access_token(data={"sub": str(user.id)})
        manager.set_cookie(response, access_token)
        return {"message": "Logged in successfully."}
    raise HTTPException(status_code=401, detail="Invalid username or password.")


@router.post("/register", status_code=201)
def api_register(data: RegisterRequest):
    if not data.username or not data.password:
        raise HTTPException(status_code=400, detail="Username and password required.")
    if models.get_user_by_username(data.username):
        raise HTTPException(status_code=409, detail="Username already exists.")

    user_id = models.create_user(data.username, data.password)
    if user_id:
        return {"message": "Registration successful."}
    raise HTTPException(status_code=500, detail="Registration failed.")


@router.post("/logout")
def api_logout(response: Response, user=Depends(get_current_user)):
    response.delete_cookie("session")
    return {"message": "Logged out successfully."}
