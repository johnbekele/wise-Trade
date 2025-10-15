from app.repositories.auth_repository import AuthRepository
from app.schemas.auth_schema import AuthTokenRead
from app.core.security import security_manager
from typing import Optional

class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()
        self.security_manager = security_manager
    async def create_token(self, token: str, user_id: str, token_type: str):
        if token_type == "email_verification":
            token=await self.security_manager.create_verification_token(user_id)
        elif token_type == "password_reset":
            token=await self.security_manager.create_reset_token(user_id)
        elif token_type == "refresh":
            token=await self.security_manager.create_refresh_token(user_id)
        elif token_type == "access":
            token=await self.security_manager.create_access_token(user_id)
        else:
            raise ValueError("Invalid token type")
        await self.auth_repository.create_token(token, user_id, token_type)
        return AuthTokenRead(**token, user_id=user_id, token_type=token_type)
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