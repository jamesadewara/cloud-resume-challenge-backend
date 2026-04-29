from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import lifespan
from app.api.routers import health, visits
from mangum import Mangum

import os

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    redoc_url=None,
    root_path="/prod" if os.getenv("AWS_EXECUTION_ENV") else ""
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return HTMLResponse(f"""
<!DOCTYPE html>
<html>
  <head>
    <title>{settings.APP_NAME} - API Docs</title>
    <meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1">
  </head>
  <body>
    <redoc spec-url="/openapi.json"></redoc>
    <script src="https://unpkg.com/redoc@latest/bundles/redoc.standalone.js"></script>
  </body>
</html>
""")

app.include_router(health.router, prefix="/api")
app.include_router(visits.router, prefix="/api")

handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)