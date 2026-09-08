from fastapi import APIRouter, Depends
from routers.auth_deps import get_current_user
import os

router = APIRouter(prefix="/api/admin")

def read_doc_file(filename: str) -> str:
    path = os.path.join(os.getcwd(), filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

@router.get("/context")
def api_admin_context(user=Depends(get_current_user)):
    """Returns local AI and human contextual knowledge synchronously."""
    # Strict admin boundaries or internal AI bounds can be further defined here.
    # Currently authenticates that a valid local session exists.
    return {
        "memory": read_doc_file("MEMORY.md"),
        "vision": read_doc_file("VISION.md"),
        "roadmap": read_doc_file("ROADMAP.md"),
        "todo": read_doc_file("TODO.md"),
        "changelog": read_doc_file("CHANGELOG.md"),
        "handoff": read_doc_file("HANDOFF.md"),
    }
