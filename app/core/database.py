from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

client: AsyncIOMotorClient | None = None
database: AsyncIOMotorDatabase | None = None


async def connect_to_mongo():
    """Create database connection"""
    global client, database
    client = AsyncIOMotorClient(settings.mongo_uri)
    database = client[settings.mongo_db_name]


async def close_mongo_connection():
    """Close database connection"""
    global client
    if client:
        client.close()


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    if database is None:
        raise RuntimeError("Database not initialized")
    return database 