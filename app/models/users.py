import asyncio
from typing import Optional
from pydantic import BaseModel, EmailStr,Field
from beanie import Document, Indexed
from datetime import datetime

class User(Document):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = Field(default=False)
    is_super_Admin: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    verification_token: Optional[str] = None
    reset_token: Optional[str] = None
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    class Settings:
        name = "users"

        class Config:
            schema_extra = {
                "example": {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "password": "password"
                }
            }