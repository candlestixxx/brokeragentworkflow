from pydantic import BaseModel
from typing import List, Optional


# --- Auth / User Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(BaseModel):
    username: str
    password: str


class UserSettingsUpdate(BaseModel):
    notifications_enabled: Optional[bool] = None
    is_public: Optional[bool] = None


class UserAvatarUpdate(BaseModel):
    avatar_url: str


# --- Goal Schemas ---
class SubGoalResponse(BaseModel):
    id: int
    description: str


class GoalResponse(BaseModel):
    id: int
    description: str
    subgoals: List[SubGoalResponse] = []
    parent_id: Optional[int] = None
    status: Optional[str] = None


class GoalCreate(BaseModel):
    description: str
    parent_id: Optional[int] = None


class GoalBreakdownRequest(BaseModel):
    description: str


# --- Habit Schemas ---
class HabitCreate(BaseModel):
    description: str


class HabitResponse(BaseModel):
    id: int
    description: str
    current_streak: int
    highest_streak: int
    last_completed_date: Optional[str] = None


# --- Initiative Schemas ---
class InitiativeCreate(BaseModel):
    quarter: str
    description: str


class InitiativeResponse(BaseModel):
    id: int
    quarter: str
    description: str
