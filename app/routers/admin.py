from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.repositories.users_repository import UsersRepository
from app.core.security import security_manager
from app.schemas.user_schema import UserRead, UserUpdate
from datetime import datetime

router = APIRouter()
bearer_scheme = HTTPBearer()


class AdminUserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    is_super_Admin: bool = False
    is_verified: bool = True
    ai_access_blocked: bool = False


class AdminUserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_super_Admin: Optional[bool] = None
    is_verified: Optional[bool] = None
    ai_access_blocked: Optional[bool] = None


class AdminPasswordUpdate(BaseModel):
    new_password: str


class UserAdminResponse(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: str
    is_active: bool
    is_super_Admin: bool
    is_verified: bool
    ai_access_blocked: bool
    auth_provider: str = "email"
    created_at: datetime
    updated_at: datetime


def get_users_repository() -> UsersRepository:
    return UsersRepository()


async def get_current_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    users_repo: UsersRepository = Depends(get_users_repository)
):
    # Verify admin access
    token = credentials.credentials
    result = security_manager.decode_token(token)
    if not result.get("success"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=result.get("message", "Invalid token"))
    
    payload = result.get("payload", {})
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    
    user = await users_repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not user.is_super_Admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    
    return user


@router.get("/users", response_model=List[UserAdminResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    admin: dict = Depends(get_current_admin_user),
    users_repo: UsersRepository = Depends(get_users_repository)
):
    # Get all users with pagination
    users = await users_repo.model.find_all().skip(skip).limit(limit).to_list()
    return [
        UserAdminResponse(
            id=str(user.id),
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_active=user.is_active,
            is_super_Admin=user.is_super_Admin,
            is_verified=user.is_verified,
            ai_access_blocked=getattr(user, 'ai_access_blocked', False),
            auth_provider=getattr(user, 'auth_provider', 'email'),
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        for user in users
    ]


@router.post("/users", response_model=UserAdminResponse)
async def create_user(
    user_data: AdminUserCreate,
    admin: dict = Depends(get_current_admin_user),
    users_repo: UsersRepository = Depends(get_users_repository)
):
    # Create new user as admin
    existing_user = await users_repo.find_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    existing_username = await users_repo.find_by_username(user_data.username)
    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    
    hashed_password = security_manager.get_password_hash(user_data.password)
    user_dict = {
        "username": user_data.username,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "is_active": True,
        "is_super_Admin": user_data.is_super_Admin,
        "is_verified": user_data.is_verified,
        "ai_access_blocked": user_data.ai_access_blocked,
        "auth_provider": "email",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    new_user = await users_repo.create(user_dict)
    return UserAdminResponse(
        id=str(new_user.id),
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        is_active=new_user.is_active,
        is_super_Admin=new_user.is_super_Admin,
        is_verified=new_user.is_verified,
        ai_access_blocked=getattr(new_user, 'ai_access_blocked', False),
        auth_provider=getattr(new_user, 'auth_provider', 'email'),
        created_at=new_user.created_at,
        updated_at=new_user.updated_at
    )


@router.get("/users/{user_id}", response_model=UserAdminResponse)
async def get_user(
    user_id: str,
    admin: dict = Depends(get_current_admin_user),
    users_repo: UsersRepository = Depends(get_users_repository)
):
    # Get user by ID
    user = await users_repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return UserAdminResponse(
        id=str(user.id),
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_super_Admin=user.is_super_Admin,
        is_verified=user.is_verified,
        ai_access_blocked=getattr(user, 'ai_access_blocked', False),
        auth_provider=getattr(user, 'auth_provider', 'email'),
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.put("/users/{user_id}", response_model=UserAdminResponse)
async def update_user(
    user_id: str,
    user_data: AdminUserUpdate,
    admin: dict = Depends(get_current_admin_user),
    users_repo: UsersRepository = Depends(get_users_repository)
):
    # Update user fields
    user = await users_repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    update_data = user_data.model_dump(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.now()
        for key, value in update_data.items():
            setattr(user, key, value)
        await user.save()
    
    return UserAdminResponse(
        id=str(user.id),
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_super_Admin=user.is_super_Admin,
        is_verified=user.is_verified,
        ai_access_blocked=getattr(user, 'ai_access_blocked', False),
        auth_provider=getattr(user, 'auth_provider', 'email'),
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.put("/users/{user_id}/password")
async def update_user_password(
    user_id: str,
    password_data: AdminPasswordUpdate,
    admin: dict = Depends(get_current_admin_user),
    users_repo: UsersRepository = Depends(get_users_repository)
):
    # Update user password
    user = await users_repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    hashed_password = security_manager.get_password_hash(password_data.new_password)
    user.hashed_password = hashed_password
    user.updated_at = datetime.now()
    await user.save()
    
    return {"message": "Password updated successfully", "user_id": user_id}


@router.put("/users/{user_id}/block-ai")
async def toggle_ai_access(
    user_id: str,
    blocked: bool,
    admin: dict = Depends(get_current_admin_user),
    users_repo: UsersRepository = Depends(get_users_repository)
):
    # Toggle AI access for user
    user = await users_repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.ai_access_blocked = blocked
    user.updated_at = datetime.now()
    await user.save()
    
    action = "blocked" if blocked else "unblocked"
    return {"message": f"AI access {action} for user", "user_id": user_id, "ai_access_blocked": blocked}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    admin: dict = Depends(get_current_admin_user),
    users_repo: UsersRepository = Depends(get_users_repository)
):
    # Delete user
    user = await users_repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if str(user.id) == str(admin.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete your own account")
    
    await user.delete()
    return {"message": "User deleted successfully", "user_id": user_id}


@router.get("/stats")
async def get_admin_stats(
    admin: dict = Depends(get_current_admin_user),
    users_repo: UsersRepository = Depends(get_users_repository)
):
    # Get admin dashboard statistics
    total_users = await users_repo.model.count()
    active_users = await users_repo.model.find({"is_active": True}).count()
    verified_users = await users_repo.model.find({"is_verified": True}).count()
    admin_users = await users_repo.model.find({"is_super_Admin": True}).count()
    ai_blocked_users = await users_repo.model.find({"ai_access_blocked": True}).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "verified_users": verified_users,
        "admin_users": admin_users,
        "ai_blocked_users": ai_blocked_users
    }
