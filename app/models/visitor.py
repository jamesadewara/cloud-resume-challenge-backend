from datetime import datetime
from typing import Optional, List
from beanie import Document
from pydantic import BaseModel, Field

class VisitLog(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    page: str = Field(default="/")
    referrer: str = Field(default="direct")
    ip: Optional[str] = Field(default=None)
    user_agent: Optional[str] = Field(default=None)

class Visitor(Document):
    count: int = Field(default=0)
    visits: List[VisitLog] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "visitors"

class VisitRequest(BaseModel):
    page: str = Field(default="/")
    referrer: str = Field(default="direct")

class VisitResponse(BaseModel):
    count: int
    message: str = Field(default="Visit recorded successfully")

class CountResponse(BaseModel):
    count: int
    last_updated: Optional[datetime] = Field(default=None)

class DetailsResponse(BaseModel):
    count: int
    total_visits: int
    recent_visits: List[VisitLog]

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    mongodb: str
