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

    async def create_token(self, token: str, payload: TokenPayload, token_type: str):

        if token_type == "email_verification":
            token=await self.security_manager.create_verification_token(payload.sub)
        elif token_type == "password_reset":
            token=await self.security_manager.create_reset_token(payload.sub)
        elif token_type == "refresh":
            token=await self.security_manager.create_refresh_token(payload)
        elif token_type == "access":
            token=await self.security_manager.create_access_token(payload)
        else:
            raise ValueError("Invalid token type")
        await self.auth_repository.create_token(token, payload.sub, token_type)
        return AuthTokenRead(**token, user_id=payload.sub, token_type=token_type)


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
                        await self.users_repository.update_user(user_id, user)
                        return user
        return None




    async def login(self, username: str, password: str)->Optional[LoginResponse]:
        print(f"User input :username={username} , password={password}")
        if "@" in username and ("." in username or ".com" in username):
            user =await self.users_repository.find_by_email(username)
        else:
            user =await self.users_repository.find_by_username(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not user.is_verified:
            raise HTTPException(status_code=401, detail="User not verified")
        if not user.is_active:
            raise HTTPException(status_code=401, detail="User not active")
        if not user.is_super_Admin:
            raise HTTPException(status_code=401, detail="User not super admin")
        if not user.is_verified:
            raise HTTPException(status_code=401, detail="User not verified")
        if not user.is_active:
            raise HTTPException(status_code=401 , detail="User not active")
            
        password_match = security_manager.verify_password(password, user.hashed_password)
        if not password_match:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        payload = TokenPayload(sub=user.id, first_name=user.first_name, last_name=user.last_name, email=user.email)

        access_token = await self.create_token(payload.sub, "access")
        refresh_token = await self.create_token(payload, "refresh")

        return LoginResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer", user=payload)

    async def send_email_verification(self, user_id: str)->Optional[str]:
        user =await self.users_repository.find_by_id(user_id)
        if user:
            verification_token = await self.security_manager.create_verification_token(user_id)
            await self.auth_repository.create_token(verification_token, user_id, "email_verification")
            
            #send verification email
            verification_link = f"{settings.FRONTEND_URL}/api/auth/verify-email?token={verification_token}"
            body = self.email_serveice.get_template("email_verification")
            body = body.replace("[Verification Link]", verification_link)
            body = body.replace("[User Name]", user.username)
            await self.email_serveice.send_email(user.email, "Email Verification", body)
        return None
      
 


    