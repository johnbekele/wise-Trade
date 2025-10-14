from typing import Type
from beanie import Document
from .base_repository import BaseRepository
from app.models.users import User
from app.schemas.user_schema import UserCreate , UserRead, UserUpdate


class UsersRepository(BaseRepository):
    def __init__(self, model: type[Document]):
        super().__init__(User)
    
    async def create_user(self, user_data:dict ,hashed_password:str)-> UserRead:
        user_data["hashed_password"]=hashed_password
        user= await self.create(user_data)
        return UserRead(**user.dict())
    async def find_by_email(self,email:str)-> UserRead | None:
        user= await self.model.find_one({"email":email})
        if user:
            return UserRead(**user.dict())
        return None
    async def find_by_username(self,username:str)-> UserRead | None:
        user= await self.model.find_one({"username":username})
        if user:
            return UserRead(**user.dict())
        return None
    async def get_user_by_id(self,user_id:str)-> UserRead | None:
        user= await self.get_by_id(user_id)
        if user:
            return UserRead(**user.dict())
        return None
    async def get_all_users(self)-> list[UserRead]:
        users= await self.get_all()
        return [UserRead(**user.dict()) for user in users]
        
    
