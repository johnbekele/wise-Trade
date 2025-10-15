from fastapi import APIRouter , Depends
from app.services.users_service import UserService
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from typing import List


router = APIRouter()
def get_user_service() -> UserService:
    return UserService()

@router.post("/create-user", response_model=UserRead)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> UserRead:
    return await user_service.create_user(user_data)


@router.post("/get-user/{user_id}", response_model=UserRead)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
) -> UserRead:
    return await user_service.get_user_by_id(user_id)

@router.get("/", response_model=List[UserRead])
async def get_all_users(
    user_service: UserService = Depends(get_user_service)
) -> List[UserRead]:
    return await user_service.get_all_users()

@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
) -> UserRead:
    return await user_service.delete_user(user_id)

