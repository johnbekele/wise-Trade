from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from app.services.api_key_service import ApiKeyService
from app.schemas.api_key_schema import (
    ApiKeyCreateRequest,
    ApiKeyCreateResponse,
    ApiKeyRead,
    ApiKeyListResponse,
    ApiKeyDeleteResponse
)
from app.core.security import security_manager
from app.repositories.users_repository import UsersRepository

router = APIRouter()
bearer_scheme = HTTPBearer(auto_error=False)


def get_api_key_service() -> ApiKeyService:
    return ApiKeyService()


def get_users_repository() -> UsersRepository:
    return UsersRepository()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> Dict[str, Any]:
    """Get current user from JWT token"""
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = credentials.credentials
    result = security_manager.decode_token(token)
    
    if not result.get("success"):
        raise HTTPException(status_code=401, detail="Invalid token")
    
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
    
    return {"user_id": user_id, "user": user}


@router.post("/", response_model=ApiKeyCreateResponse)
async def create_api_key(
    request: ApiKeyCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    api_key_service: ApiKeyService = Depends(get_api_key_service)
):
    """Create a new API key for the authenticated user"""
    user_id = current_user["user_id"]
    
    full_key, api_key = await api_key_service.create_api_key(
        user_id=user_id,
        name=request.name,
        expires_days=request.expires_days
    )
    
    return ApiKeyCreateResponse(
        api_key=full_key,
        id=str(api_key.id),
        name=api_key.name,
        key_prefix=api_key.key_prefix,
        created_at=api_key.created_at,
        expires_at=api_key.expires_at
    )


@router.get("/", response_model=ApiKeyListResponse)
async def list_api_keys(
    current_user: Dict[str, Any] = Depends(get_current_user),
    api_key_service: ApiKeyService = Depends(get_api_key_service)
):
    """List all API keys for the authenticated user"""
    user_id = current_user["user_id"]
    api_keys = await api_key_service.get_user_api_keys(user_id)
    
    return ApiKeyListResponse(
        api_keys=[
            ApiKeyRead(
                id=str(key.id),
                name=key.name,
                key_prefix=key.key_prefix,
                is_active=key.is_active,
                created_at=key.created_at,
                last_used_at=key.last_used_at,
                expires_at=key.expires_at
            )
            for key in api_keys
        ]
    )


@router.delete("/{api_key_id}", response_model=ApiKeyDeleteResponse)
async def delete_api_key(
    api_key_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    api_key_service: ApiKeyService = Depends(get_api_key_service)
):
    """Delete an API key"""
    user_id = current_user["user_id"]
    await api_key_service.delete_api_key(api_key_id, user_id)
    
    return ApiKeyDeleteResponse(
        message="API key deleted successfully",
        api_key_id=api_key_id
    )

