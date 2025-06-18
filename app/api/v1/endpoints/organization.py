from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_database
from app.crud.organization import create_organization, get_organization_by_name, organization_exists_by_slug
from app.crud.user import create_admin_in_org
from app.schemas.organization import (
    OrganizationCreateRequest,
    OrganizationCreateResponse,
    OrganizationGetResponse
)
from slugify import slugify

router = APIRouter()


@router.post("/create", response_model=OrganizationCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_org(
    request: OrganizationCreateRequest,
    db = Depends(get_database)
):
    """Create organization endpoint"""
    # Check if organization already exists
    existing_org = await get_organization_by_name(db, request.organization_name)
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization already exists"
        )
    
    # Check if slug already exists
    slug = slugify(request.organization_name)
    if await organization_exists_by_slug(db, slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization slug already exists"
        )
    
    # Create organization
    created_slug = await create_organization(
        db=db,
        name=request.organization_name,
        admin_email=request.email
    )
    
    # Create admin in organization-specific collection
    await create_admin_in_org(
        db=db,
        slug=created_slug,
        email=request.email,
        password=request.password
    )
    
    return OrganizationCreateResponse(
        organization_name=request.organization_name,
        slug=created_slug
    )


@router.get("/get", response_model=OrganizationGetResponse)
async def get_org(
    organization_name: str,
    db = Depends(get_database)
):
    """Get organization endpoint"""
    org = await get_organization_by_name(db, organization_name)
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    return OrganizationGetResponse(
        organization_name=org.name,
        slug=org.slug
    ) 