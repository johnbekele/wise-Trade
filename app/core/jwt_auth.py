"""
JWT-only authentication for frontend requests.
This is the native authentication method for the web application.
"""
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from app.core.security import security_manager
from app.repositories.users_repository import UsersRepository

bearer_scheme = HTTPBearer()


def get_users_repository() -> UsersRepository:
    return UsersRepository()


async def authenticate_jwt_only(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> Dict[str, Any]:
    """
    Authenticate user using JWT token only.
    This is for frontend requests - API keys are NOT accepted here.
    """
    token = credentials.credentials
    
    # Decode JWT token
    result = security_manager.decode_token(token)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=401, 
            detail="Invalid or expired JWT token. Please login again."
        )
    
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


async def check_ai_access_jwt_only(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> Dict[str, Any]:
    """
    Authenticate with JWT and check AI access.
    For frontend requests only.
    """
    auth_result = await authenticate_jwt_only(credentials)
    user = auth_result["user"]
    
    # Check if user has AI access blocked
    if getattr(user, 'ai_access_blocked', False):
        raise HTTPException(
            status_code=403,
            detail="Your AI access has been blocked. Please contact an administrator."
        )
    
    return auth_result

