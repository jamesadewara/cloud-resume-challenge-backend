from datetime import datetime
from fastapi import APIRouter
from app.models.visitor import HealthResponse

router = APIRouter(tags=["Health"])

@router.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify API and database connectivity."""
    return HealthResponse(
        status="ok",
        timestamp=datetime.utcnow(),
        mongodb="connected"
    )
