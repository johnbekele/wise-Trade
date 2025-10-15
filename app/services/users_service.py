from site import USER_BASE
from typing import Optional, List
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.repositories.users_repository import UsersRepository
from datetime import datetime
from fastapi import HTTPException
from app.core.security import security_manager
from app.repositories.auth_repository import AuthRepository
from app.services.email_service import EmailService
from app.core.config import settings


class UserService():
    def __init__(self):
        self.init="UserService initialized"
        self.users_repository = UsersRepository()
        self.auth_repository = AuthRepository()
        self.email_service = EmailService()

    async def create_user(self, user_data: UserCreate)-> Optional[UserRead]:
        exisiting_user = await self.users_repository.find_by_email(user_data.email)
        username_exists = await self.users_repository.find_by_username(user_data.username)

        if exisiting_user:
            if exisiting_user.is_verified:
                raise HTTPException(status_code=400, detail="User already exists")
            else:
                raise HTTPException(status_code=400, detail="User already exists but not verified")
        if username_exists:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        hashed_password = security_manager.get_password_hash(user_data.password)
        user_data.is_verified = False
        user_data.is_active = False
        user_data.is_super_Admin = False
        
        user = await self.users_repository.create_user(user_data.model_dump(), hashed_password)
        print("user created successfully")
        # Create verification token after user is created (when we have the user id)
        print("creating verification token")
        verification_token = security_manager.create_verification_token(str(user.id))
        await self.auth_repository.create_token(verification_token, str(user.id), "email_verification")
        print("verification token created successfully")
        

        #send verification email 
        email_service = EmailService()
        verification_link = f"{settings.FRONTEND_URL}/api/auth/verify-email?token={verification_token}"
        body = email_service.get_template("email_verification")
        body = body.replace("[Verification Link]", verification_link)
        body = body.replace("[User Name]", user_data.username)
        await email_service.send_email(
            to_email=user_data.email,
            subject="Email Verification - Resent",
            body=body,
        )
        # user is already a UserRead object from the repository
        return user
    async def get_all_users(self)-> List[UserRead]:
        return await self.users_repository.get_all_users()
    
    async def get_user_by_id(self, user_id: str)-> UserRead:
        return await self.users_repository.get_user_by_id(user_id)
    
    async def update_user(self, user_id: str, user_data: UserUpdate)-> UserRead:
        return await self.users_repository.update_user(user_id, user_data)
    
    async def delete_user(self, user_id: str)-> UserRead:
        return await self.users_repository.delete_user(user_id)