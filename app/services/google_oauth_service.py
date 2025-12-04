from typing import Optional, Dict, Any
import requests
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from app.core.config import settings
from app.repositories.users_repository import UsersRepository
from app.models.users import User
from datetime import datetime
import uuid


class GoogleOAuthService:
    def __init__(self):
        self.users_repository = UsersRepository()
        self.oauth = self._setup_oauth()
    
    def _setup_oauth(self) -> OAuth:
        oauth = OAuth()
        oauth.register(
            name="google",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            authorize_url="https://accounts.google.com/o/oauth2/auth",
            authorize_params=None,
            access_token_url="https://accounts.google.com/o/oauth2/token",
            access_token_params=None,
            refresh_token_url=None,
            authorize_state=settings.SECRET_KEY,
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
            jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
            client_kwargs={"scope": "openid profile email"},
        )
        return oauth
    
    async def get_authorization_url(self, request: Request) -> RedirectResponse:
        # Get authorization URL and redirect to Google
        referer = request.headers.get("referer")
        if referer:
            request.session["login_redirect"] = referer
        elif settings.FRONTEND_URL:
            request.session["login_redirect"] = settings.FRONTEND_URL
        else:
            request.session["login_redirect"] = "http://localhost:3000"
        
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        return await self.oauth.google.authorize_redirect(request, redirect_uri, prompt="consent")
    
    async def handle_callback(self, request: Request) -> Dict[str, Any]:
        # Handle Google OAuth callback
        try:
            token = await self.oauth.google.authorize_access_token(request)
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Google authentication failed: {str(e)}")
        
        try:
            user_info_endpoint = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {"Authorization": f'Bearer {token["access_token"]}'}
            google_response = requests.get(user_info_endpoint, headers=headers, timeout=5)
            google_response.raise_for_status()
            user_info = google_response.json()
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Failed to fetch user info from Google: {str(e)}")
        
        user_data = token.get("userinfo", {})
        user_id = user_data.get("sub")
        iss = user_data.get("iss")
        user_email = user_data.get("email") or user_info.get("email")
        user_name = user_info.get("name", "")
        user_pic = user_info.get("picture")
        
        if iss not in ["https://accounts.google.com", "accounts.google.com"]:
            raise HTTPException(status_code=401, detail="Invalid token issuer")
        
        if not user_id or not user_email:
            raise HTTPException(status_code=401, detail="Missing required user information")
        
        user = await self._find_or_create_user(google_id=user_id, email=user_email, name=user_name, profile_picture=user_pic)
        return {"user": user, "google_token": token, "user_info": user_info}
    
    async def _find_or_create_user(self, google_id: str, email: str, name: str, profile_picture: Optional[str] = None) -> User:
        # Find or create user by Google ID
        user = await User.find_one(User.google_id == google_id)
        
        if user:
            user.updated_at = datetime.now()
            if profile_picture and user.profile_picture != profile_picture:
                user.profile_picture = profile_picture
            await user.save()
            return user
        
        user = await User.find_one(User.email == email)
        
        if user:
            user.google_id = google_id
            user.auth_provider = "google"
            user.is_verified = True
            user.profile_picture = profile_picture
            user.updated_at = datetime.now()
            await user.save()
            return user
        
        name_parts = name.split(" ", 1)
        first_name = name_parts[0] if name_parts else name
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        username = email.split("@")[0]
        existing_user = await User.find_one(User.username == username)
        if existing_user:
            username = f"{username}_{uuid.uuid4().hex[:6]}"
        
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            google_id=google_id,
            profile_picture=profile_picture,
            auth_provider="google",
            is_verified=True,
            is_active=True,
            hashed_password=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        await new_user.insert()
        return new_user
    
    def get_redirect_url(self, request: Request) -> str:
        return request.session.pop("login_redirect", settings.FRONTEND_URL or "http://localhost:3000")
