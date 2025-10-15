# core/security.py
from datetime import datetime, timedelta, timezone  # Fixed: removed duplicate datetime
from typing import Optional, Dict, Any
from jose import JWTError, jwt , ExpiredSignatureError, JWSError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings
import requests
import time


class SecurityManager:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.refresh_key = settings.REFRESH_SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, plain_password: str) -> str:
        """Hash password"""
        return self.pwd_context.hash(plain_password)

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()  # Copy user data to avoid modification
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.access_token_expire_minutes
            )

        to_encode.update({"exp": int(expire.timestamp())})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        """Create refresh JWT token"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=self.refresh_token_expire_days
        )
        to_encode.update({"exp": expire})  # Fixed: added expiration
        encoded_jwt = jwt.encode(to_encode, self.refresh_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[str]:
        """Verify JWT token and return username"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: Optional[str] = payload.get("sub")
            if username is None:
                return None
            return username
        except JWTError:
            return None
    def verify_apple_token(identity_token: str, client_id: str) -> Optional[str]:
        try:
            # Fetch Apple's public keys
            apple_key_url = "https://appleid.apple.com/auth/keys"
            response = requests.get(apple_key_url)
            response.raise_for_status()
            jwks = response.json()

            header = jwt.get_unverified_header(identity_token)
            kid = header.get("kid")
            alg = header.get("alg")
    
            key =next((k for k in jwks if k["id"] == kid ), None)

            if key is None:
                print("No matching key found")
                return None
            
            public_key = jwt.construct_rsa_key(key)


    
            # Decode the token using Apple's key
            payload = jwt.decode(
               identity_token,
                public_key,
                algorithms=[alg],
                audience=client_id,
            )
    
            return payload.get("sub")  # unique user ID
            
        except Exception as e:
            print("Apple token verification failed:", e)
            return None
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return {"success": True, "payload": payload}
        except ExpiredSignatureError:
            message = "Token has expired"
            return {"success": False, "message": message}
        except JWSError as e:
            message = f"JWT Error: {e}"
            return {"success": False, "message": message}
        except Exception as e:
            message = f"JWT Error: {e}"
            return {"success": False, "message": message}

    def refresh_access_token(self, refresh_token: str) -> str:
        """Create new access token from refresh token"""
        try:
            payload = jwt.decode(
                refresh_token, self.secret_key, algorithms=[self.algorithm]
            )
            username: Optional[str] = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )

            # Create new access token
            access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
            new_token = self.create_access_token(
                data={"sub": username}, expires_delta=access_token_expires
            )
            return new_token

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

    def create_verification_token(self, user_id: str) -> str:
        """Create verification token"""
        payload = {"sub": user_id}
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        payload.update({"exp": expire})
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_reset_token(self, user_id: str) -> str:
        """Create reset token"""
        payload = {"sub": user_id}
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        payload.update({"exp": expire})
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
# Fixed: Added parentheses to instantiate the class
security_manager = SecurityManager()
