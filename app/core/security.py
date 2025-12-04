from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt, ExpiredSignatureError, JWSError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings
import requests


class SecurityManager:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.refresh_key = settings.REFRESH_SECRET_KEY
        self.algorithm = settings.ALGORITHM or "HS256"
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        if not self.secret_key:
            raise ValueError("SECRET_KEY is not set in environment variables")
        if not self.refresh_key:
            raise ValueError("REFRESH_SECRET_KEY is not set in environment variables")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, plain_password: str) -> str:
        return self.pwd_context.hash(plain_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": int(expire.timestamp())})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.refresh_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: Optional[str] = payload.get("sub")
            return username if username else None
        except JWTError:
            return None

    def verify_apple_token(identity_token: str, client_id: str) -> Optional[str]:
        # Verify Apple Sign In token
        try:
            apple_key_url = "https://appleid.apple.com/auth/keys"
            response = requests.get(apple_key_url)
            response.raise_for_status()
            jwks = response.json()

            header = jwt.get_unverified_header(identity_token)
            kid = header.get("kid")
            alg = header.get("alg")
            key = next((k for k in jwks if k["id"] == kid), None)

            if key is None:
                return None
            
            public_key = jwt.construct_rsa_key(key)
            payload = jwt.decode(identity_token, public_key, algorithms=[alg], audience=client_id)
            return payload.get("sub")
        except Exception as e:
            return None

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return {"success": True, "payload": payload}
        except ExpiredSignatureError:
            return {"success": False, "message": "Token has expired"}
        except JWSError as e:
            return {"success": False, "message": f"JWT Error: {e}"}
        except Exception as e:
            return {"success": False, "message": f"JWT Error: {e}"}

    def refresh_access_token(self, refresh_token: str) -> str:
        try:
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=[self.algorithm])
            username: Optional[str] = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
            access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
            return self.create_access_token(data={"sub": username}, expires_delta=access_token_expires)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    def create_verification_token(self, user_id: str) -> str:
        payload = {"sub": user_id}
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        payload.update({"exp": expire})
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_reset_token(self, user_id: str) -> str:
        payload = {"sub": user_id}
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        payload.update({"exp": expire})
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_access_token_from_google_user(self, user_id: str, email: str, expires_delta: Optional[timedelta] = None) -> str:
        data = {"sub": user_id, "email": email, "auth_provider": "google"}
        return self.create_access_token(data, expires_delta)

    def get_current_user_from_cookie(self, token: Optional[str] = None) -> Dict[str, Any]:
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated - no token provided")
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            
            if not user_id or not email:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
            
            return {"user_id": user_id, "email": email, "auth_provider": payload.get("auth_provider", "email")}
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired. Please login again.")
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}")


security_manager = SecurityManager()
