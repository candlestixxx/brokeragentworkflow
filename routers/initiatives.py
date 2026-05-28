from fastapi import APIRouter, Depends, HTTPException
from auth_utils import get_current_user
import models
import schemas

router = APIRouter(prefix="/api/initiatives")


@router.get("")
def get_initiatives(current_user: models.User = Depends(get_current_user)):
    initiatives = models.list_pending_initiatives(user_id=current_user.id)
    results = [{"id": i[0], "quarter": i[1], "description": i[2]} for i in initiatives]
    return {"initiatives": results}


@router.post("", status_code=201)
def add_initiative(
    init_data: schemas.InitiativeCreate,
    current_user: models.User = Depends(get_current_user),
):
    init_id = models.add_initiative(
        init_data.quarter, init_data.description, user_id=current_user.id
    )
    return {"message": "Initiative added.", "id": init_id}


@router.post("/{initiative_id}/complete")
def complete_initiative(
    initiative_id: int, current_user: models.User = Depends(get_current_user)
):
    success = models.complete_initiative(initiative_id, user_id=current_user.id)
    if success:
        return {"message": f"Initiative {initiative_id} completed."}
    raise HTTPException(status_code=404, detail="Initiative not found.")
