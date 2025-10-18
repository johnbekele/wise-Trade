from pydantic import BaseModel ,EmailStr , validator    
from typing import Literal , Optional 
from datetime import datetime

class AuthTokenRead(BaseModel):
    token: str
    token_type: Literal["access", "refresh" ,"password_reset","email_verification"]
    user_id: str
    created_at: datetime
    expires_at: datetime


class TokenPayload(BaseModel):
    sub: str
    first_name:Optional[str] = None
    last_name:Optional[str] = None
    email:Optional[str] = None
    exp:Optional[int] = None
    
    
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"]
    user: TokenPayload
    

class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]

class LoginRequest(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
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

