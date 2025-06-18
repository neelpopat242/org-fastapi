from __future__ import annotations

from datetime import datetime
from slugify import slugify
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.organization import OrganizationInDB


async def create_organization(
    db: AsyncIOMotorDatabase,
    name: str,
    admin_email: str
) -> str:
    """Create organization and return slug"""
    slug = slugify(name)
    
    org_doc = OrganizationInDB(
        name=name,
        slug=slug,
        admin_email=admin_email,
        created_at=datetime.utcnow()
    )
    
    # Insert into ORG collection
    await db.ORG.insert_one(org_doc.model_dump())
    
    return slug


async def get_organization_by_name(
    db: AsyncIOMotorDatabase,
    name: str
) -> OrganizationInDB | None:
    """Get organization by name"""
    org_doc = await db.ORG.find_one({"name": name})
    if org_doc:
        return OrganizationInDB(**org_doc)
    return None


async def organization_exists_by_slug(
    db: AsyncIOMotorDatabase,
    slug: str
) -> bool:
    """Check if organization exists by slug"""
    count = await db.ORG.count_documents({"slug": slug})
    return count > 0 