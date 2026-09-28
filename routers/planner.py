import extensions
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import models
from routers.auth_deps import get_current_user
from notifications import notify_all

router = APIRouter(prefix="/api/planner")

class MacroPlanRequest(BaseModel):
    plan_type: str
    period_name: str
    description: str

@router.get("")
def api_get_macro_plans(user=Depends(get_current_user)):
    plans = models.list_macro_plans(user_id=user.id)
    return {"plans": plans}

@router.post("", status_code=201)
def api_add_macro_plan(data: MacroPlanRequest, user=Depends(get_current_user)):
    if not data.plan_type or not data.period_name or not data.description:
         raise HTTPException(status_code=400, detail="All fields are required.")
    if data.plan_type not in ["yearly", "quarterly", "monthly", "weekly"]:
         raise HTTPException(status_code=400, detail="Invalid plan type.")

    plan_id = models.add_macro_plan(data.plan_type, data.period_name, data.description, user_id=user.id)

    notify_all(
        subject="New Macro Plan Added",
        body=f"You added a new {data.plan_type} plan for {data.period_name}.",
        speakable_message=f"You added a new {data.plan_type} plan for {data.period_name}.",
    )
    extensions.sync_emit(
        "data_updated", {"message": "Plan added"}, to=str(user.id)
    )

    return {"message": "Plan created.", "id": plan_id}

@router.post("/{plan_id}/complete")
def api_complete_macro_plan(plan_id: int, user=Depends(get_current_user)):
    success = models.complete_macro_plan(plan_id, user_id=user.id)
    if success:
        extensions.sync_emit(
            "data_updated", {"message": "Plan completed"}, to=str(user.id)
        )
        return {"message": f"Plan {plan_id} completed."}
    raise HTTPException(status_code=404, detail="Plan not found.")

@router.delete("/{plan_id}")
def api_delete_macro_plan(plan_id: int, user=Depends(get_current_user)):
    success = models.delete_macro_plan(plan_id, user_id=user.id)
    if success:
        extensions.sync_emit(
            "data_updated", {"message": "Plan deleted"}, to=str(user.id)
        )
        return {"message": f"Plan {plan_id} deleted."}
    raise HTTPException(status_code=404, detail="Plan not found.")
