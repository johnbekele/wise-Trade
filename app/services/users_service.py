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
from app.services.auth_service import AuthService
from app.schemas.auth_schema import EmailVerificationResponse 
from beanie import PydanticObjectId
class UserService():
    def __init__(self):
        self.init="UserService initialized"
        self.users_repository = UsersRepository()
        self.auth_repository = AuthRepository()
        self.email_service = EmailService()
        self.auth_service = AuthService()

    async def create_user(self, user_data: UserCreate)-> Optional[UserRead]:
        exisiting_user = await self.users_repository.find_by_email(user_data.email)
        username_exists = await self.users_repository.find_by_username(user_data.username)

        if exisiting_user:
            raise HTTPException(status_code=400, detail="User already exists")
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
        
        # Explicit debugging
        print("=" * 80)
        print("🔍 EMAIL VERIFICATION LINK GENERATION DEBUG")
        print("=" * 80)
        print(f"1. settings.FRONTEND_URL = {repr(settings.FRONTEND_URL)}")
        
        frontend_url = settings.FRONTEND_URL or "http://localhost:3002"
        print(f"2. frontend_url (after fallback) = {repr(frontend_url)}")
        
        verification_link = f"{frontend_url}/verify-email?token={verification_token}"
        print(f"3. Final verification_link = {repr(verification_link)}")
        print("=" * 80)
        
        body = email_service.get_template("email_verification")
        body = body.replace("[Verification Link]", verification_link)
        body = body.replace("[User Name]", user_data.username)
        
        # Check what's actually in the body
        import re
        links = re.findall(r'href="([^"]+)"', body)
        print(f"4. Links found in email body: {links}")
        print("=" * 80)
        
        await email_service.send_email(
            to_email=user_data.email,
            subject="Email Verification - Wise Trade",
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
    
    async def delete_user(self, user_id: str) -> UserRead:
        # Try to get user data before deletion
        user = await self.users_repository.get_user_by_id(user_id)
        
        if not user:
            # If we can't find the user by ID, try to find by other means
            # This handles cases where Beanie can't find the user due to data inconsistencies
            try:
                from app.models.users import User
                from beanie import PydanticObjectId
                
                # Try direct MongoDB query as fallback
                user_direct = await User.find_one({"_id": PydanticObjectId(user_id)})
                if user_direct:
                    # Create a UserRead object from the direct query result
                    user_dict = user_direct.to_dict_with_id()
                    user = UserRead(**user_dict, message="User found via direct query")
                else:
                    raise HTTPException(status_code=404, detail="User not found")
            except Exception as e:
                raise HTTPException(status_code=404, detail="User not found")
        
        # Delete the user
        try:
            await self.users_repository.delete_user(user_id)
        except Exception as e:
            # Even if delete fails, return the user data we found
            pass
        
        # Return the user data that was deleted
        return user