from typing import Optional
from beanie import Document, Indexed
from pydantic import BaseModel, Field
from datetime import datetime
import secrets


class ApiKey(Document):
    """API Key model for user API access"""
    key: str = Field(..., description="The API key (hashed)")
    key_prefix: str = Field(..., description="First 8 characters for display")
    user_id: Indexed(str) = Field(..., description="User who owns this API key")
    name: str = Field(..., description="User-friendly name for the API key")
    is_active: bool = Field(default=True, description="Whether the key is active")
    created_at: datetime = Field(default_factory=datetime.now)
    last_used_at: Optional[datetime] = Field(default=None, description="Last time the key was used")
    expires_at: Optional[datetime] = Field(default=None, description="Optional expiration date")
    
    class Settings:
        name = "api_keys"
        indexes = [
            "user_id",
            "key_prefix",
        ]

