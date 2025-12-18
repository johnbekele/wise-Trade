"""
API Key-only authentication for external API users.
This is for programmatic access - JWT tokens are NOT accepted here.
"""
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from app.services.api_key_service import ApiKeyService
from app.repositories.users_repository import UsersRepository

bearer_scheme = HTTPBearer()


def get_api_key_service() -> ApiKeyService:
    return ApiKeyService()


def get_users_repository() -> UsersRepository:
    return UsersRepository()


async def authenticate_api_key_only(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> Dict[str, Any]:
    """
    Authenticate using API key only.
    This is for external API users - JWT tokens are NOT accepted here.
    API keys must start with "wt_" prefix.
    """
    token = credentials.credentials
    
    # API keys must start with "wt_"
    if not token.startswith("wt_"):
        raise HTTPException(
            status_code=401, 
            detail="Invalid API key format. API keys must start with 'wt_'. This endpoint only accepts API keys, not JWT tokens."
        )
    
    api_key_service = get_api_key_service()
    api_key_doc = await api_key_service.validate_api_key(token)
    
    if not api_key_doc:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Get user information
    users_repo = get_users_repository()
    user = await users_repo.find_by_id(api_key_doc.user_id)
    
    if not user:
        raise HTTPException(status_code=401, detail="User associated with API key not found")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is inactive")
    
    return {
        "user_id": str(user.id),
        "user": user,
        "auth_method": "api_key"
    }


async def check_ai_access_api_key_only(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> Dict[str, Any]:
    """
    Authenticate with API key and check AI access.
    For external API users only.
    """
    auth_result = await authenticate_api_key_only(credentials)
    user = auth_result["user"]
    
    # Check if user has AI access blocked
    if getattr(user, 'ai_access_blocked', False):
        raise HTTPException(
            status_code=403,
            detail="Your AI access has been blocked. Please contact an administrator."
        )
    
    return auth_result

