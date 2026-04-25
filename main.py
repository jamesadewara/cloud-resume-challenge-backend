# ============================================
# James Adewara Resume - Visitor Counter API
# FastAPI + Beanie (Pydantic ODM) + MongoDB
# ============================================

import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Document, Indexed, init_beanie
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# ============================================
# CONFIGURATION
# ============================================
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/resume_counter")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# ============================================
# BEANIE DOCUMENT MODELS
# ============================================

class VisitLog(BaseModel):
    """Individual visit record embedded in Visitor document."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    page: str = "/"
    referrer: str = "direct"
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None


class Visitor(Document):
    """Main visitor counter document — singleton, only one exists."""
    count: int = 0
    visits: list[VisitLog] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "visitors"


# ============================================
# PYDANTIC REQUEST/RESPONSE MODELS
# ============================================

class VisitRequest(BaseModel):
    page: str = "/"
    referrer: str = "direct"


class VisitResponse(BaseModel):
    count: int
    message: str = "Visit recorded successfully"


class CountResponse(BaseModel):
    count: int
    last_updated: Optional[datetime] = None


class DetailsResponse(BaseModel):
    count: int
    total_visits: int
    recent_visits: list[VisitLog]


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    mongodb: str


# ============================================
# LIFESPAN (startup / shutdown)
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    client = AsyncIOMotorClient(MONGODB_URI)
    await init_beanie(
        database=client.get_default_database(),
        document_models=[Visitor]
    )

    # Initialize singleton counter if not exists
    existing = await Visitor.find_one()
    if not existing:
        await Visitor(count=0, visits=[]).insert()
        print("✅ Visitor counter initialized in MongoDB")
    else:
        print(f"✅ Counter exists. Current count: {existing.count}")

    app.state.db_client = client
    yield

    # Shutdown
    client.close()
    print("🔌 MongoDB connection closed")


# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title="James Adewara Resume API",
    description="MongoDB-backed visitor counter for resume website",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ============================================
# API ROUTES
# ============================================

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        timestamp=datetime.utcnow(),
        mongodb="connected"
    )


@app.get("/api/visits", response_model=CountResponse)
async def get_visits():
    """Get current total visitor count."""
    doc = await Visitor.find_one()
    if not doc:
        return CountResponse(count=0)
    return CountResponse(
        count=doc.count,
        last_updated=doc.updated_at
    )


@app.post("/api/visit", response_model=VisitResponse)
async def record_visit(request: Request, body: VisitRequest):
    """Record a new visit and increment counter."""

    visit = VisitLog(
        timestamp=datetime.utcnow(),
        page=body.page,
        referrer=body.referrer,
        ip=request.headers.get("x-forwarded-for") or request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    doc = await Visitor.find_one()
    if not doc:
        doc = Visitor(count=1, visits=[visit])
        await doc.insert()
    else:
        doc.count += 1
        doc.visits.append(visit)
        doc.updated_at = datetime.utcnow()
        await doc.save()

    return VisitResponse(count=doc.count)


@app.get("/api/visits/details", response_model=DetailsResponse)
async def get_visit_details():
    """Get detailed analytics (last 50 visits)."""
    doc = await Visitor.find_one()
    if not doc:
        return DetailsResponse(count=0, total_visits=0, recent_visits=[])

    recent = sorted(doc.visits, key=lambda v: v.timestamp, reverse=True)[:50]

    return DetailsResponse(
        count=doc.count,
        total_visits=len(doc.visits),
        recent_visits=recent
    )


# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)