from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import AsyncMongoClient
from beanie import init_beanie

from app.core.config import settings
from app.models.visitor import Visitor

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"📡 Connecting to MongoDB: {settings.MONGODB_URL}")
    try:
        client = AsyncMongoClient(settings.MONGODB_URL)
        await init_beanie(database=client[settings.DB_NAME], document_models=[Visitor])
        print("✅ Beanie ODM initialized")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        raise

    existing = await Visitor.find_one()
    if not existing:
        await Visitor(count=0, visits=[]).insert()
        print("✅ Initialized counter")

    yield
    print("🔌 Connection closed")
