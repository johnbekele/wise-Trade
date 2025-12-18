from typing import Optional, List
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.repositories.api_key_repository import ApiKeyRepository
from app.models.api_key import ApiKey
from app.core.security import security_manager
import secrets
import hashlib


class ApiKeyService:
    def __init__(self):
        self.api_key_repository = ApiKeyRepository()
    
    def generate_api_key(self) -> tuple[str, str]:
        """Generate a new API key and return (full_key, hashed_key, prefix)"""
        # Generate a secure random key (32 bytes = 64 hex characters)
        full_key = f"wt_{secrets.token_urlsafe(32)}"
        # Hash the key for storage
        hashed_key = hashlib.sha256(full_key.encode()).hexdigest()
        # Store prefix for display (first 8 chars after "wt_")
        key_prefix = full_key[:10]  # "wt_" + 7 chars
        return full_key, hashed_key, key_prefix
    
    async def create_api_key(self, user_id: str, name: str, expires_days: Optional[int] = None) -> tuple[str, ApiKey]:
        """Create a new API key for a user"""
        full_key, hashed_key, key_prefix = self.generate_api_key()
        
        expires_at = None
        if expires_days:
            expires_at = datetime.now() + timedelta(days=expires_days)
        
        api_key_data = {
            "key": hashed_key,
            "key_prefix": key_prefix,
            "user_id": user_id,
            "name": name,
            "is_active": True,
            "created_at": datetime.now(),
            "expires_at": expires_at
        }
        
        api_key = await self.api_key_repository.create(api_key_data)
        return full_key, api_key
    
    async def validate_api_key(self, api_key: str) -> Optional[ApiKey]:
        """Validate an API key and return the ApiKey document if valid"""
        # Hash the provided key
        hashed_key = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Find the API key
        api_key_doc = await self.api_key_repository.find_by_key_hash(hashed_key)
        
        if not api_key_doc:
            return None
        
        # Check if key is active
        if not api_key_doc.is_active:
            raise HTTPException(status_code=403, detail="API key is inactive")
        
        # Check if key is expired
        if api_key_doc.expires_at and api_key_doc.expires_at < datetime.now():
            raise HTTPException(status_code=403, detail="API key has expired")
        
        # Update last used timestamp
        await self.api_key_repository.update_last_used(str(api_key_doc.id))
        
        return api_key_doc
    
    async def get_user_api_keys(self, user_id: str) -> List[ApiKey]:
        """Get all API keys for a user"""
        return await self.api_key_repository.find_by_user_id(user_id)
    
    async def delete_api_key(self, api_key_id: str, user_id: str) -> bool:
        """Delete an API key (only if owned by user)"""
        api_key = await self.api_key_repository.find_by_id(api_key_id)
        
        if not api_key:
            raise HTTPException(status_code=404, detail="API key not found")
        
        if api_key.user_id != user_id:
            raise HTTPException(status_code=403, detail="You don't have permission to delete this API key")
        
        await self.api_key_repository.delete(api_key_id)
        return True
    
    async def deactivate_api_key(self, api_key_id: str, user_id: str) -> bool:
        """Deactivate an API key (only if owned by user)"""
        api_key = await self.api_key_repository.find_by_id(api_key_id)
        
        if not api_key:
            raise HTTPException(status_code=404, detail="API key not found")
        
        if api_key.user_id != user_id:
            raise HTTPException(status_code=403, detail="You don't have permission to modify this API key")
        
        api_key.is_active = False
        await api_key.save()
        return True

