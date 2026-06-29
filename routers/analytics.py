from fastapi import APIRouter, Depends
import models
from routers.auth_deps import get_current_user

router = APIRouter()


@router.get("/api/analytics")
def get_analytics(user=Depends(get_current_user)):
    stats = models.get_user_analytics(user.id)
    return stats


@router.get("/api/me/heatmap")
def get_heatmap(user=Depends(get_current_user)):
    data = models.get_user_heatmap(user.id)
    return data
