from pydantic import BaseModel
from typing import Literal , Optional
from datetime import datetime

class AuthTokenRead(BaseModel):
    token: str
    token_type: Literal["access", "refresh" ,"password_reset","email_verification"]
    user_id: str
    created_at: datetime
    expires_at: datetime
    