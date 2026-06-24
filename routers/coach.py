from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import time
from routers.auth_deps import get_current_user

router = APIRouter(prefix="/api/coach")


class CoachRequest(BaseModel):
    goal_description: str


def generate_mock_suggestions(description: str):
    """Simulate an LLM AI Coach breaking down a complex goal."""
    desc = description.lower()
    if "workout" in desc or "fitness" in desc or "gym" in desc:
        return [
            "Pack gym bag the night before.",
            "Drink 500ml of water immediately upon waking.",
            "Do a 5-minute dynamic warm-up.",
        ]
    elif "code" in desc or "program" in desc or "app" in desc:
        return [
            "Write a failing test first (TDD).",
            "Break the feature into 3 small functions.",
            "Commit working code every 15 minutes.",
        ]
    elif "read" in desc or "book" in desc:
        return [
            "Read just 1 page to build momentum.",
            "Leave the book on your pillow.",
            "Turn off your phone 30 minutes before bed.",
        ]
    else:
        return [
            f"Define the very first 2-minute action for '{description}'.",
            "Set a 15-minute timer and work with no distractions.",
            "Review your progress at the end of the day.",
        ]


@router.post("/suggest")
def api_coach_suggest(data: CoachRequest, user=Depends(get_current_user)):
    if not data.goal_description:
        raise HTTPException(status_code=400, detail="Goal description is required.")

    # Simulate AI processing delay
    time.sleep(1)

    suggestions = generate_mock_suggestions(data.goal_description)

    return {"suggestions": suggestions}
