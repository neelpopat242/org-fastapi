from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.database import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


app = FastAPI(
    title="Organization API",
    description="API for managing organizations and admin authentication",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Organization API is running"} 