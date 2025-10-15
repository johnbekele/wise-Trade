from fastapi import APIRouter , Depends
from app.services.users_service import UserService
from app.core.config import settings
from app.schemas.user_schema import UserCreate
router = APIRouter()

@router.get("/")
def test():
    return {"message": "Hello, router is working!"}

@router.get("/user")
async def get_user():
    user_service = UserService()
    users = await user_service.get_all_users()
    return {"message": "Users retrieved successfully", "data": users}

@router.post("/user")
async def create_user(user: UserCreate ,user_service: UserService = Depends(UserService)):
    result = await user_service.create_user(user)
    return {"message": "User created successfully", "data": result}

@router.get("/config")
def get_config():
    return {"message": "Configuration endpoint - credentials hidden for security"}