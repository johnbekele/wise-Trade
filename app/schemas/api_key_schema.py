from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ApiKeyCreateRequest(BaseModel):
    name: str
    expires_days: Optional[int] = None


class ApiKeyCreateResponse(BaseModel):
    api_key: str  # The full key (only shown once)
    id: str
    name: str
    key_prefix: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    message: str = "API key created successfully. Save this key now - it won't be shown again!"


class ApiKeyRead(BaseModel):
    id: str
    name: str
    key_prefix: str
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class ApiKeyListResponse(BaseModel):
    api_keys: list[ApiKeyRead]


class ApiKeyDeleteResponse(BaseModel):
    message: str
    api_key_id: str

