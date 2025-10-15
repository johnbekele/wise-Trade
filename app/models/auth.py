from beanie import Document
from datetime import datetime
from typing import Literal

class AuthToken(Document):
    token: str
    token_type: Literal["access", "refresh" ,"password_reset","email_verification"]
    user_id: str
    created_at: datetime
    expires_at: datetime

    class Settings:
        name = "auth_tokens"