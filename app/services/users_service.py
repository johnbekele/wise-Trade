from typing import Optional, List
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.repositories.test_repo import TestRepository
from datetime import datetime

class UserService():
    def __init__(self):
        self.init="UserService initialized"
        self.test_repository = TestRepository()
    async def get_all_users(self) -> Optional[List[UserRead]]:
        documents = await self.test_repository.get_all_users()
        return documents
    async def create_user(self, user: UserCreate):
        # Map schema fields to model fields
        user_data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "hashed_password": user.password,  # In production, hash this password
            "is_active": False,
            "is_super_Admin": False,
            "is_verified": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        result = await self.test_repository.create_user(user_data)
        return result