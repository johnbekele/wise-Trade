from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from app.core.security import security_manager
from app.services.api_key_service import ApiKeyService
from app.repositories.users_repository import UsersRepository

bearer_scheme = HTTPBearer(auto_error=False)


def get_api_key_service() -> ApiKeyService:
    return ApiKeyService()


def get_users_repository() -> UsersRepository:
    return UsersRepository()


async def authenticate_user_or_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)
) -> Dict[str, Any]:
    """
    Authenticate user using either JWT token or API key.
    Returns user information if authenticated.
    """
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required. Provide a Bearer token or API key.")
    
    token = credentials.credentials
    
    # Try API key authentication first (API keys start with "wt_")
    if token.startswith("wt_"):
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
    
    # Try JWT token authentication
    result = security_manager.decode_token(token)
    
    if not result.get("success"):
        raise HTTPException(status_code=401, detail="Invalid token or API key")
    
    payload = result.get("payload", {})
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    users_repo = get_users_repository()
    user = await users_repo.find_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is inactive")
    
    return {
        "user_id": user_id,
        "user": user,
        "auth_method": "jwt"
    }


async def check_ai_access_with_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)
) -> Dict[str, Any]:
    """
    Authenticate and check AI access using either JWT token or API key.
    """
    auth_result = await authenticate_user_or_api_key(credentials)
    user = auth_result["user"]
    
    # Check if user has AI access blocked
    if getattr(user, 'ai_access_blocked', False):
        raise HTTPException(
            status_code=403,
            detail="Your AI access has been blocked. Please contact an administrator."
        )
    
    return auth_result

