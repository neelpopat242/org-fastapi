from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.database import get_database
from app.core.security import decode_token
from app.crud.user import get_admin_from_org
from app.schemas.user import AdminInDB

security = HTTPBearer()


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_database)
) -> tuple[AdminInDB, str]:
    """Get current authenticated admin"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(credentials.credentials)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    slug: str = payload.get("slug")
    
    if email is None or slug is None:
        raise credentials_exception
    
    admin = await get_admin_from_org(db, slug, email)
    if admin is None:
        raise credentials_exception
    
    return admin, slug 