"""
Beanie ODM Models for Resume Counter API
========================================
Defines MongoDB document schemas and request/response models.
"""

from datetime import datetime
from typing import Optional, List

from beanie import Document
from pydantic import BaseModel, Field


# ============================================
# BEANIE DOCUMENT MODELS (MongoDB)
# ============================================

class VisitLog(BaseModel):
    """Individual visit record embedded in Visitor document."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    page: str = Field(default="/", description="Page path visited")
    referrer: str = Field(default="direct", description="HTTP referrer")
    ip: Optional[str] = Field(default=None, description="Visitor IP address")
    user_agent: Optional[str] = Field(default=None, description="Browser user agent")
    country: Optional[str] = Field(default=None, description="GeoIP country")
    city: Optional[str] = Field(default=None, description="GeoIP city")


class Visitor(Document):
    """
    Main visitor counter document — singleton collection with one document.
    Tracks total visits, recent visit details, and metadata.
    """
    count: int = Field(default=0, description="Total visitor count")
    visits: List[VisitLog] = Field(default_factory=list, description="Recent visit logs")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Document creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    class Settings:
        name = "visitors"  # MongoDB collection name
        description = "Visitor counter singleton document"


# ============================================
# PYDANTIC REQUEST/RESPONSE MODELS
# ============================================

class VisitRequest(BaseModel):
    """Request body for recording a new visit."""
    page: str = Field(default="/", description="Page path")
    referrer: str = Field(default="direct", description="HTTP referrer")
    
    class Config:
        json_schema_extra = {
            "example": {
                "page": "/resume",
                "referrer": "google.com"
            }
        }


class VisitResponse(BaseModel):
    """Response after recording a visit."""
    count: int = Field(description="Updated total visitor count")
    message: str = Field(default="Visit recorded successfully")
    
    class Config:
        json_schema_extra = {
            "example": {
                "count": 42,
                "message": "Visit recorded successfully"
            }
        }


class CountResponse(BaseModel):
    """Response with current visitor count."""
    count: int = Field(description="Total visitor count")
    last_updated: Optional[datetime] = Field(default=None, description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "count": 42,
                "last_updated": "2024-04-26T12:00:00"
            }
        }


class DetailsResponse(BaseModel):
    """Detailed response with count and recent visits."""
    count: int = Field(description="Total visitor count")
    total_visits: int = Field(description="Total number of visits in history")
    recent_visits: List[VisitLog] = Field(description="Most recent visits")
    
    class Config:
        json_schema_extra = {
            "example": {
                "count": 42,
                "total_visits": 42,
                "recent_visits": [
                    {
                        "timestamp": "2024-04-26T12:00:00",
                        "page": "/resume",
                        "referrer": "google.com"
                    }
                ]
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(description="Service status")
    timestamp: datetime = Field(description="Response timestamp")
    mongodb: str = Field(description="MongoDB connection status")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "timestamp": "2024-04-26T12:00:00",
                "mongodb": "connected"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str = Field(description="Error message")
    status_code: int = Field(description="HTTP status code")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Internal server error",
                "status_code": 500,
                "timestamp": "2024-04-26T12:00:00"
            }
        }
