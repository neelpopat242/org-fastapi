from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str = Field(default="mongodb://localhost:27017", env="MONGO_URI")
    mongo_db_name: str = Field(default="org_service", env="MONGO_DB_NAME")
    jwt_secret_key: str = Field(env="JWT_SECRET_KEY")
    access_token_expire_minutes: int = Field(default=15, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings() 