from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.security import hash_password
from app.schemas.user import AdminInDB


async def create_admin_in_org(
    db: AsyncIOMotorDatabase,
    slug: str,
    email: str,
    password: str
) -> None:
    """Create admin in organization-specific collection"""
    collection_name = f"{slug}_admins"
    
    admin_doc = AdminInDB(
        email=email,
        hashed_password=hash_password(password)
    )
    
    await db[collection_name].insert_one(admin_doc.model_dump())


async def find_admin_across_orgs(
    db: AsyncIOMotorDatabase,
    email: str
) -> tuple[AdminInDB, str] | None:
    """Find admin across all organization admin collections"""
    # Get all collection names
    collection_names = await db.list_collection_names()
    admin_collections = [name for name in collection_names if name.endswith("_admins")]
    
    for collection_name in admin_collections:
        admin_doc = await db[collection_name].find_one({"email": email})
        if admin_doc:
            slug = collection_name.replace("_admins", "")
            return AdminInDB(**admin_doc), slug
    
    return None


async def get_admin_from_org(
    db: AsyncIOMotorDatabase,
    slug: str,
    email: str
) -> AdminInDB | None:
    """Get admin from specific organization collection"""
    collection_name = f"{slug}_admins"
    admin_doc = await db[collection_name].find_one({"email": email})
    if admin_doc:
        return AdminInDB(**admin_doc)
    return None 