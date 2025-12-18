from typing import Optional, List
from beanie import Document
from .base_repository import BaseRepository
from app.models.api_key import ApiKey


class ApiKeyRepository(BaseRepository):
    def __init__(self):
        super().__init__(ApiKey)
    
    async def find_by_key_hash(self, key_hash: str) -> Optional[ApiKey]:
        """Find API key by hashed key"""
        return await self.find_one({"key": key_hash})
    
    async def find_by_user_id(self, user_id: str) -> List[ApiKey]:
        """Find all API keys for a user"""
        return await self.model.find({"user_id": user_id}).to_list()
    
    async def find_by_key_prefix(self, key_prefix: str) -> Optional[ApiKey]:
        """Find API key by prefix (for display purposes)"""
        return await self.find_one({"key_prefix": key_prefix})
    
    async def update_last_used(self, api_key_id: str) -> Optional[ApiKey]:
        """Update the last_used_at timestamp"""
        from datetime import datetime
        api_key = await self.find_by_id(api_key_id)
        if api_key:
            api_key.last_used_at = datetime.now()
            await api_key.save()
        return api_key

