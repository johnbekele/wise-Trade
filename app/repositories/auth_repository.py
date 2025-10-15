from .base_repository import BaseRepository
from app.models.auth import AuthToken
from typing import Literal , Optional
from app.schemas.auth_schema import AuthTokenRead

class AuthRepository(BaseRepository):
    def __init__(self):
        super().__init__(AuthToken)
    
    async def create_token(self, token: str, user_id: str, token_type: str):
        from datetime import datetime, timedelta
        token_data = {
            "token": token,
            "user_id": user_id,
            "token_type": token_type,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(minutes=15)  # 15 minutes expiry
        }
        return await self.create(token_data)
    
    async def find_by_token(self, token: str)-> Optional[AuthTokenRead]:
        return await self.model.find_one({"token": token})
    
   