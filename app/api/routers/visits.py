from datetime import datetime
from fastapi import APIRouter, Request

from app.models.visitor import (
    Visitor,
    VisitLog,
    VisitRequest,
    VisitResponse,
    CountResponse,
    DetailsResponse,
)

router = APIRouter(tags=["Visitors"])

@router.get("/api/visits", response_model=CountResponse)
async def get_visits():
    """Get current total visitor count."""
    doc = await Visitor.find_one()
    if not doc:
        return CountResponse(count=0)
    return CountResponse(
        count=doc.count,
        last_updated=doc.updated_at
    )


@router.post("/api/visit", response_model=VisitResponse)
async def record_visit(request: Request, body: VisitRequest):
    """Record a new visit and increment the counter."""
    
    # Create visit log entry
    visit = VisitLog(
        timestamp=datetime.utcnow(),
        page=body.page,
        referrer=body.referrer,
        ip=request.headers.get("x-forwarded-for") or (request.client.host if request.client else None),
        user_agent=request.headers.get("user-agent")
    )

    # Update or create visitor document
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


@router.get("/api/visits/details", response_model=DetailsResponse)
async def get_visit_details():
    """Get detailed analytics including recent visits."""
    doc = await Visitor.find_one()
    if not doc:
        return DetailsResponse(count=0, total_visits=0, recent_visits=[])

    recent = sorted(doc.visits, key=lambda v: v.timestamp, reverse=True)[:50]

    return DetailsResponse(
        count=doc.count,
        total_visits=len(doc.visits),
        recent_visits=recent
    )
