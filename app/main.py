# ============================================
# James Adewara Resume - Visitor Counter API
# FastAPI + Beanie (Pydantic ODM) + PyMongo
# ============================================

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import lifespan
from app.api.routers import health, visits

# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title="James Adewara Resume API",
    description="MongoDB-backed visitor counter for resume website",
    version="1.0.0",
    lifespan=lifespan,
    redoc_url=None,  # Disable default redoc to use custom CDN
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ============================================
# API ROUTES
# ============================================

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    # Serves ReDoc using unpkg CDN instead of jsdelivr.net
    # jsdelivr is blocked by Edge/Safari tracking prevention
    return HTMLResponse(f"""
<!DOCTYPE html>
<html>
  <head>
    <title>{settings.APP_NAME} - API Docs</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body {{ margin: 0; padding: 0; }}</style>
  </head>
  <body>
    <redoc spec-url="/openapi.json"></redoc>
    <script src="https://unpkg.com/redoc@latest/bundles/redoc.standalone.js"></script>
  </body>
</html>
""")

app.include_router(health.router)
app.include_router(visits.router)

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)