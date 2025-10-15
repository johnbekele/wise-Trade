import asyncio
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from beanie import Document, Indexed
from datetime import datetime
from bson import ObjectId

class User(Document):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = Field(default=False)
    is_super_Admin: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    reset_token: Optional[str] = None
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    
    def to_dict_with_id(self) -> dict:
        """Convert to dict with string id"""
        data = self.model_dump()
        # In Beanie, the id is available in the dict after insertion
        if "id" in data and data["id"]:
            data["id"] = str(data["id"])
        else:
            data["id"] = ""
        return data

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