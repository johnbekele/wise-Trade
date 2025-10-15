from typing import Type , Optional
from beanie import Document
from .base_repository import BaseRepository
from app.models.users import User
from app.schemas.user_schema import UserCreate , UserRead, UserUpdate


class UsersRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
    
    async def create_user(self, user_data:dict ,hashed_password:str)-> UserRead:
        user_data["hashed_password"]=hashed_password
        user= await self.create(user_data)
        user_dict = user.to_dict_with_id()
        return UserRead(**user_dict, message="account created successfully please check your email for verification")
    async def find_by_email(self,email:str)-> UserRead | None:
        user= await self.model.find_one({"email":email})
        if user:
            user_dict = user.to_dict_with_id()
            return UserRead(**user_dict, message="User found")
        return None
    async def find_by_username(self,username:str)-> UserRead | None:
        user= await self.model.find_one({"username":username})
        if user:
            user_dict = user.to_dict_with_id()
            return UserRead(**user_dict, message="User found")
        return None
    async def get_user_by_id(self,user_id:str)-> UserRead | None:
        user= await self.get_by_id(user_id)
        if user:
            user_dict = user.to_dict_with_id()
            return UserRead(**user_dict, message="User found")
        return None
    async def get_all_users(self,skip:int =0 ,limit:int =100)-> list[UserRead]:
        users= await self.get_all(skip,limit)
        return [UserRead(**user.to_dict_with_id(), message="User found") for user in users]
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> UserRead:
        user = await self.update(user_id, user_data.model_dump(exclude_unset=True))
        if user:
            user_dict = user.to_dict_with_id()
            return UserRead(**user_dict, message="User updated successfully")
        return None
    async def delete_user(self ,user_id:str)-> Optional[UserRead]:
        user= await self.delete(user_id)
        if user:
            user_dict = user.to_dict_with_id()
            return UserRead(**user_dict, message="User deleted successfully")
        return None
        
    
