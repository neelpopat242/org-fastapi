from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_database
from app.core.security import verify_password, create_access_token
from app.crud.user import find_admin_across_orgs
from app.schemas.user import AdminLoginRequest
from app.schemas.token import Token

router = APIRouter()


@router.post("/login", response_model=Token)
async def admin_login(
    request: AdminLoginRequest,
    db = Depends(get_database)
):
    """Admin login endpoint"""
    admin_result = await find_admin_across_orgs(db, request.admin)
    
    if not admin_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    admin, slug = admin_result
    
    if not verify_password(request.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(subject=admin.email, slug=slug)
    
    return Token(access_token=access_token, token_type="bearer") 