from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str 
    is_active: bool = False
    is_super_Admin: bool = False
    is_verified: bool = False
    ai_access_blocked: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    


class UserRead(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    hashed_password: Optional[str] = None
    email: EmailStr
    is_active: bool
    is_super_Admin: bool
    is_verified: bool
    ai_access_blocked: bool = False
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
    ai_access_blocked: Optional[bool] = None

class UserDeleteResponse(BaseModel):
    message: str
    user_id: str