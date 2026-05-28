from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth_utils import (
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
import models
import schemas
from datetime import timedelta

router = APIRouter(prefix="/api")


@router.post("/login")
def login(user_data: schemas.UserLogin):
    user = models.get_user_by_username(user_data.username)
    if not user or not user.check_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Logged in successfully.",
    }


@router.post("/login_form")
def login_form(form_data: OAuth2PasswordRequestForm = Depends()):
    user = models.get_user_by_username(form_data.username)
    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", status_code=201)
def register(user_data: schemas.UserRegister):
    if models.get_user_by_username(user_data.username):
        raise HTTPException(status_code=409, detail="Username already exists.")
    user_id = models.create_user(user_data.username, user_data.password)
    if user_id:
        return {"message": "Registration successful."}
    raise HTTPException(status_code=500, detail="Registration failed.")


@router.get("/me")
def get_me(current_user: models.User = Depends(get_current_user)):
    badges = models.get_user_badges(current_user.id)
    return {
        "authenticated": True,
        "user_id": current_user.id,
        "username": current_user.username,
        "avatar_url": current_user.avatar_url,
        "notifications_enabled": current_user.notifications_enabled,
        "is_public": current_user.is_public,
        "badges": badges,
    }


@router.get("/me/analytics")
def get_me_analytics(current_user: models.User = Depends(get_current_user)):
    completed_goals = len(models.list_completed_goals(user_id=current_user.id))
    active_initiatives = len(models.list_pending_initiatives(user_id=current_user.id))
    habits = models.list_habits(user_id=current_user.id)
    total_habits = len(habits)
    longest_streak = max([h["highest_streak"] for h in habits]) if habits else 0

    return {
        "completed_goals": completed_goals,
        "active_initiatives": active_initiatives,
        "total_habits": total_habits,
        "longest_streak": longest_streak,
    }


@router.post("/me/settings")
def update_settings(
    settings: schemas.UserSettingsUpdate,
    current_user: models.User = Depends(get_current_user),
):
    if settings.notifications_enabled is None and settings.is_public is None:
        raise HTTPException(status_code=400, detail="Missing setting parameters.")

    success = models.update_user_settings(
        current_user.id, settings.notifications_enabled, settings.is_public
    )
    if success:
        return {"message": "Settings updated."}
    raise HTTPException(status_code=500, detail="Update failed.")


@router.post("/me/avatar")
def update_avatar(
    avatar_data: schemas.UserAvatarUpdate,
    current_user: models.User = Depends(get_current_user),
):
    success = models.update_user_avatar(current_user.id, avatar_data.avatar_url)
    if success:
        return {"message": "Avatar updated."}
    raise HTTPException(status_code=500, detail="Update failed.")


@router.post("/logout")
def logout():
    return {"message": "Logged out successfully."}
