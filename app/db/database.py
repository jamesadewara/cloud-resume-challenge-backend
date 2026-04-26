from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import AsyncMongoClient
from beanie import init_beanie

from app.core.config import settings
from app.models.visitor import Visitor

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle management: startup and shutdown.
    Initializes MongoDB connection via Beanie and PyMongo.
    """
    # Startup
    print(f"📡 Connecting to MongoDB: {settings.MONGODB_URL}")
    
    try:
        client = AsyncMongoClient(settings.MONGODB_URL)
        await init_beanie(
            database=client[settings.DB_NAME],
            document_models=[Visitor]
        )
        print("✅ Beanie ODM initialized successfully with PyMongo")
    except Exception as e:
        print(f"❌ Failed to initialize Beanie: {e}")
        raise

    # Initialize singleton counter if not exists
    existing = await Visitor.find_one()
    if not existing:
        await Visitor(count=0, visits=[]).insert()
        print("✅ Visitor counter initialized in MongoDB")
    else:
        print(f"✅ Counter exists. Current count: {existing.count}")

    yield

    # Shutdown
    print("🔌 MongoDB connection closed")
