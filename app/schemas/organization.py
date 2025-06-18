from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, EmailStr


class OrganizationCreateRequest(BaseModel):
    organization_name: str
    email: EmailStr
    password: str


class OrganizationCreateResponse(BaseModel):
    organization_name: str
    slug: str


class OrganizationGetRequest(BaseModel):
    organization_name: str


class OrganizationGetResponse(BaseModel):
    organization_name: str
    slug: str


class OrganizationInDB(BaseModel):
    name: str
    slug: str
    admin_email: str
    created_at: datetime 