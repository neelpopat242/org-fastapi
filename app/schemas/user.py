from __future__ import annotations

from pydantic import BaseModel, EmailStr


class AdminLoginRequest(BaseModel):
    admin: EmailStr
    password: str


class AdminInDB(BaseModel):
    email: str
    hashed_password: str 