from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str  # This will be hashed in the service layer

class UserRead(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    is_super_Admin: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_super_Admin: Optional[bool] = None
    is_verified: Optional[bool] = None