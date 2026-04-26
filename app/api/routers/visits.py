from datetime import datetime, timedelta
from fastapi import APIRouter, Request
from app.models.visitor import (
    Visitor, VisitLog, VisitRequest, VisitResponse, CountResponse, DetailsResponse
)

router = APIRouter(tags=["Visitors"])

@router.get("/api/visits", response_model=CountResponse)
async def get_visits():
    doc = await Visitor.find_one()
    if not doc:
        return CountResponse(count=0)
    return CountResponse(count=doc.count, last_updated=doc.updated_at)

@router.post("/api/visit", response_model=VisitResponse)
async def record_visit(request: Request, body: VisitRequest):
    ip = request.headers.get("x-forwarded-for") or (request.client.host if request.client else None)
    
    visit = VisitLog(
        timestamp=datetime.utcnow(),
        page=body.page,
        referrer=body.referrer,
        ip=ip,
        user_agent=request.headers.get("user-agent")
    )

    doc = await Visitor.find_one()
    if not doc:
        doc = Visitor(count=1, visits=[visit])
        await doc.insert()
    else:
        # Prevent double counting from same IP in last 24 hours
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        is_duplicate = any(
            v.ip == ip and v.timestamp > one_day_ago 
            for v in doc.visits[-100:] # Check last 100 entries for efficiency
        )
        
        if not is_duplicate:
            doc.count += 1
            
        doc.visits.append(visit)
        doc.updated_at = datetime.utcnow()
        
        # Keep only last 1000 visits to prevent document bloat
        if len(doc.visits) > 1000:
            doc.visits = doc.visits[-1000:]
            
        await doc.save()

    return VisitResponse(count=doc.count)

@router.get("/api/visits/details", response_model=DetailsResponse)
async def get_visit_details():
    doc = await Visitor.find_one()
    if not doc:
        return DetailsResponse(count=0, total_visits=0, recent_visits=[])

    recent = sorted(doc.visits, key=lambda v: v.timestamp, reverse=True)[:50]
    return DetailsResponse(count=doc.count, total_visits=len(doc.visits), recent_visits=recent)
