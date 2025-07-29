from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.user import User
from typing import Optional

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None

# MongoDB client instance
mongodb = MongoDB()

async def connect_to_mongo():
    """Create database connection and initialize Beanie"""
    mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)
    mongodb.database = mongodb.client[settings.MONGODB_DATABASE]
    
    # Initialize Beanie with User model
    await init_beanie(database=mongodb.database, document_models=[User])
    
    print(f"✅ Connected to MongoDB: {settings.MONGODB_DATABASE}")

async def close_mongo_connection():
    """Close database connection"""
    if mongodb.client:
        mongodb.client.close()
        print("❌ Disconnected from MongoDB")

def get_database():
    """Get database instance"""
    return mongodb.database
