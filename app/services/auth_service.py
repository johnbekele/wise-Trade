from fastapi import HTTPException
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth_schema import AuthTokenRead  ,TokenPayload ,LoginResponse
from app.core.security import security_manager
from typing import Optional
from app.repositories.users_repository import UsersRepository
from app.services.email_service import EmailService
from app.core.config import settings



class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()
        self.security_manager = security_manager
        self.users_repository = UsersRepository()
        self.email_serveice=EmailService()

    async def create_token(self, token: str, payload: dict, token_type: str):

        if token_type == "email_verification":
            token = self.security_manager.create_verification_token(payload["sub"])
        elif token_type == "password_reset":
            token = self.security_manager.create_reset_token(payload["sub"])
        elif token_type == "refresh":
            token = self.security_manager.create_refresh_token(payload)
        elif token_type == "access":
            token = self.security_manager.create_access_token(payload)
        else:
            raise ValueError("Invalid token type")
        await self.auth_repository.create_token(token, payload["sub"], token_type)
        return token


    async def verify_email(self, token: str)->Optional[str]:
        token_data = await self.auth_repository.find_by_token(token)
        if token_data:
            decoded_token =await self.security_manager.verify_token(token)
            if decoded_token:
                user_id = decoded_token.get("sub")
                if user_id:
                    user = await self.users_repository.find_by_id(user_id)
                    if user:
                        user.is_verified = True
                        user.is_active = True
                        await self.users_repository.update_user(user_id, user)
                        return user
        return None




    async def login(self, username: str, password: str)->Optional[LoginResponse]:
        print(f"User input :username={username} , password={password}")
        if "@" in username and ("." in username or ".com" in username):
            user = await self.users_repository.find_by_email(username)
        else:
            user = await self.users_repository.find_by_username(username)
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not user.is_verified:
            raise HTTPException(status_code=401, detail="User not verified")
        
        if not user.is_active:
            raise HTTPException(status_code=401, detail="User not active")
            
        password_match = security_manager.verify_password(password, user.hashed_password)
        if not password_match:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        payload = TokenPayload(sub=user.id, first_name=user.first_name, last_name=user.last_name, email=user.email)
        payload_dict = payload.model_dump()

        access_token = await self.create_token("", payload_dict, "access")
        refresh_token = await self.create_token("", payload_dict, "refresh")

        return LoginResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer", user=payload)

    async def send_email_verification(self, user_id: str)->str:
        try:
            user = await self.users_repository.get_user_by_id(user_id)
            if not user:
                return "User not found"
            
            user_id = str(user.id)
            verification_token = self.security_manager.create_verification_token(user_id)
            await self.auth_repository.create_token(verification_token, user_id, "email_verification")
            
            # Send verification email
            frontend_url = settings.FRONTEND_URL or "http://localhost:3000"
            verification_link = f"{frontend_url}/api/auth/verify-email?token={verification_token}"
            body = self.email_serveice.get_template("email_verification")
            body = body.replace("[Verification Link]", verification_link)
            body = body.replace("[User Name]", user.username)
            
            await self.email_serveice.send_email(user.email, "Email Verification", body)
            return "Verification email sent successfully"
            
        except Exception as e:
            print(f"Error in send_email_verification: {e}")
            import traceback
            traceback.print_exc()
            return f"Error sending verification email: {str(e)}"
    

    async def verify_email(self, token: str) -> Optional[str]:
        try:
            token_data = await self.auth_repository.find_by_token(token)
            if token_data:
                if token_data.token_type == "email_verification":
                    # Verify the token and get the user_id
                    user_id = self.security_manager.verify_token(token)
                    if user_id:
                        # Get the user document directly from the model
                        from app.models.users import User
                        from beanie import PydanticObjectId
                        
                        user_doc = await User.find_one({"_id": PydanticObjectId(user_id)})
                        if user_doc:
                            # Update the user document directly
                            user_doc.is_verified = True
                            user_doc.is_active = True
                            await user_doc.save()
                            return "Email verified successfully"
                        else:
                            return "User not found"
                    else:
                        return "Invalid token"
                else:
                    return "Invalid token type"
            else:
                return "Token not found"
        except Exception as e:
            print(f"Error in verify_email: {e}")
            import traceback
            traceback.print_exc()
            return f"Error verifying email: {str(e)}"
      
 


    