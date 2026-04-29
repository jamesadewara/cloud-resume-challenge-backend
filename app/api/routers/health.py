from datetime import datetime
from fastapi import APIRouter
from app.models.visitor import HealthResponse

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok",
        timestamp=datetime.utcnow(),
        mongodb="connected"
    )
