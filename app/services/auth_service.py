from fastapi import HTTPException, BackgroundTasks
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth_schema import AuthTokenRead, TokenPayload, LoginResponse
from app.core.security import security_manager
from typing import Optional
from app.repositories.users_repository import UsersRepository
from app.services.email_service import EmailService
from app.core.config import settings
from app.schemas.user_schema import UserRead


class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()
        self.security_manager = security_manager
        self.users_repository = UsersRepository()
        self.email_service = EmailService()

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

    async def login(self, username: str, password: str) -> Optional[LoginResponse]:
        # Login with username or email
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
        return LoginResponse(token=access_token, token_type="bearer", user=payload)

    async def send_email_verification(self, user_id: str, background_tasks=None) -> str:
        # Send verification email to user
        try:
            user = await self.users_repository.get_user_by_id(user_id)
            if not user:
                return "User not found"
            
            user_id = str(user.id)
            verification_token = self.security_manager.create_verification_token(user_id)
            await self.auth_repository.create_token(verification_token, user_id, "email_verification")
            
            frontend_url = settings.FRONTEND_URL or "http://localhost:3002"
            verification_link = f"{frontend_url}/verify-email?token={verification_token}"
            body = self.email_service.get_template("email_verification")
            body = body.replace("[Verification Link]", verification_link)
            body = body.replace("[User Name]", user.username)
            
            if background_tasks:
                background_tasks.add_task(self.email_service.send_email, to_email=user.email, subject="Email Verification - Wise Trade", body=body)
                return "Verification email queued successfully"
            else:
                await self.email_service.send_email(user.email, "Email Verification - Wise Trade", body)
                return "Verification email sent successfully"
        except Exception as e:
            return f"Error sending verification email: {str(e)}"

    async def verify_email(self, token: str) -> Optional[str]:
        # Verify email with token
        try:
            if not token:
                return "Token is required"
            
            user_id = self.security_manager.verify_token(token)
            if not user_id:
                return "Invalid or expired token"
            
            token_data = await self.auth_repository.find_by_token(token)
            if not token_data:
                return "Token not found in database"
            if token_data.token_type != "email_verification":
                return "Invalid token type"
            
            user_doc = await self.users_repository.find_by_id(user_id)
            if not user_doc:
                return "User not found"
            if user_doc.is_verified:
                return "Email already verified"
            
            user_doc.is_verified = True
            user_doc.is_active = True
            await user_doc.save()
            
            try:
                await self.auth_repository.delete_token(token)
            except:
                pass
            
            return "Email verified successfully"
        except Exception as e:
            return f"Error verifying email: {str(e)}"

    async def find_by_token(self, token: str):
        # Find user by JWT token
        try:
            decoded_token = self.security_manager.decode_token(token)
            if decoded_token["success"]:
                payload = decoded_token["payload"]
                user_id = payload["sub"]
                user = await self.users_repository.find_by_id(user_id)
                if user:
                    user_dict = user.to_dict_with_id()
                    return UserRead(**user_dict, message="User found")
            return None
        except Exception as e:
            return None

    async def request_password_reset(self, email: str, background_tasks=None) -> str:
        # Request password reset by email
        try:
            user_read = await self.users_repository.find_by_email(email)
            if not user_read:
                return "If an account with that email exists, a password reset link has been sent."
            
            user_doc = await self.users_repository.find_by_id(user_read.id)
            if not user_doc:
                return "If an account with that email exists, a password reset link has been sent."
            
            user_id = str(user_doc.id)
            reset_token = self.security_manager.create_reset_token(user_id)
            await self.auth_repository.create_token(reset_token, user_id, "password_reset")
            
            frontend_url = settings.FRONTEND_URL or "http://localhost:3000"
            reset_link = f"{frontend_url}/reset-password?token={reset_token}"
            body = self.email_service.get_template("password_reset")
            body = body.replace("[Reset Link]", reset_link)
            body = body.replace("[User Name]", user_doc.username)
            
            if background_tasks:
                background_tasks.add_task(self.email_service.send_email, to_email=email, subject="Password Reset - Wise Trade", body=body)
            else:
                await self.email_service.send_email(email, "Password Reset - Wise Trade", body)
            return "If an account with that email exists, a password reset link has been sent."
        except Exception as e:
            return "If an account with that email exists, a password reset link has been sent."

    async def confirm_password_reset(self, token: str, new_password: str) -> str:
        # Confirm password reset with token
        try:
            if not token:
                return "Token is required"
            
            user_id = self.security_manager.verify_token(token)
            if not user_id:
                return "Invalid or expired token"
            
            token_data = await self.auth_repository.find_by_token(token)
            if not token_data:
                return "Token not found in database"
            if token_data.token_type != "password_reset":
                return "Invalid token type"
            
            user_doc = await self.users_repository.find_by_id(user_id)
            if not user_doc:
                return "User not found"
            
            hashed_password = self.security_manager.get_password_hash(new_password)
            user_doc.hashed_password = hashed_password
            await user_doc.save()
            
            try:
                await self.auth_repository.delete_token(token)
            except:
                pass
            
            return "Password reset successfully"
        except Exception as e:
            return f"Error resetting password: {str(e)}"

    async def resend_verification_by_email(self, email: str, background_tasks=None) -> str:
        # Resend verification email
        try:
            user_read = await self.users_repository.find_by_email(email)
            if not user_read:
                return "If an account with that email exists, a verification link has been sent."
            
            user_doc = await self.users_repository.find_by_id(user_read.id)
            if not user_doc:
                return "If an account with that email exists, a verification link has been sent."
            if user_doc.is_verified:
                return "Email is already verified"
            
            user_id = str(user_doc.id)
            verification_token = self.security_manager.create_verification_token(user_id)
            await self.auth_repository.create_token(verification_token, user_id, "email_verification")
            
            frontend_url = settings.FRONTEND_URL or "http://localhost:3000"
            verification_link = f"{frontend_url}/verify-email?token={verification_token}"
            body = self.email_service.get_template("email_verification")
            body = body.replace("[Verification Link]", verification_link)
            body = body.replace("[User Name]", user_doc.username)
            
            if background_tasks:
                background_tasks.add_task(self.email_service.send_email, to_email=email, subject="Email Verification - Wise Trade", body=body)
            else:
                await self.email_service.send_email(email, "Email Verification - Wise Trade", body)
            return "If an account with that email exists, a verification link has been sent."
        except Exception as e:
            return "If an account with that email exists, a verification link has been sent."
