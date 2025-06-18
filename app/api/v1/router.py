from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import auth, organization

api_router = APIRouter()

api_router.include_router(organization.router, prefix="/org", tags=["organizations"])
api_router.include_router(auth.router, prefix="/admin", tags=["authentication"]) 