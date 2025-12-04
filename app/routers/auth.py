from app.schemas.user_schema import UserRead
from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks, Request, Cookie
from fastapi.responses import RedirectResponse, JSONResponse
from app.services.auth_service import AuthService
from app.services.google_oauth_service import GoogleOAuthService
from app.schemas.auth_schema import LoginResponse, LoginRequest, GoogleAuthResponse, PasswordResetRequest, PasswordResetConfirm, ResendVerificationRequest
from app.core.security import security_manager
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from datetime import timedelta

router = APIRouter()
bearer_scheme = HTTPBearer()


def get_auth_service() -> AuthService:
    return AuthService()


def get_google_oauth_service() -> GoogleOAuthService:
    return GoogleOAuthService()


def get_current_user_from_cookie(access_token: Optional[str] = Cookie(None)) -> Dict[str, Any]:
    return security_manager.get_current_user_from_cookie(access_token)


@router.post("/login")
async def login(login_request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)) -> LoginResponse:
    return await auth_service.login(login_request.username, login_request.password)


@router.post("/resend-email-verification/{user_id}")
async def send_email_verification(user_id, background_tasks: BackgroundTasks, auth_service: AuthService = Depends(get_auth_service)) -> str:
    return await auth_service.send_email_verification(user_id, background_tasks)


@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest, background_tasks: BackgroundTasks, auth_service: AuthService = Depends(get_auth_service)):
    result = await auth_service.request_password_reset(request.email, background_tasks)
    return {"message": result}


@router.post("/reset-password")
async def reset_password(request: PasswordResetConfirm, auth_service: AuthService = Depends(get_auth_service)):
    result = await auth_service.confirm_password_reset(request.token, request.new_password)
    if result == "Password reset successfully":
        return {"message": result, "success": True}
    elif result in ["Token is required", "Invalid or expired token", "Token not found in database", "Invalid token type"]:
        raise HTTPException(status_code=400, detail=result)
    elif result == "User not found":
        raise HTTPException(status_code=404, detail=result)
    else:
        raise HTTPException(status_code=500, detail=result or "Error resetting password")


@router.post("/resend-verification")
async def resend_verification(request: ResendVerificationRequest, background_tasks: BackgroundTasks, auth_service: AuthService = Depends(get_auth_service)):
    result = await auth_service.resend_verification_by_email(request.email, background_tasks)
    if result == "Email is already verified":
        return {"message": result, "success": True, "already_verified": True}
    else:
        return {"message": result, "success": True}


@router.get("/verify-email")
async def verify_email(token: str = Query(...), auth_service: AuthService = Depends(get_auth_service)):
    result = await auth_service.verify_email(token)
    if result == "Email verified successfully":
        return {"message": result, "success": True}
    elif result == "Email already verified":
        return {"message": result, "success": True, "already_verified": True}
    elif result in ["Invalid or expired token", "Invalid token", "Token not found", "Invalid token type"]:
        raise HTTPException(status_code=400, detail=result)
    elif result == "User not found":
        raise HTTPException(status_code=404, detail=result)
    else:
        raise HTTPException(status_code=500, detail=result or "Error verifying email")


@router.get("/me")
async def user_info(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), auth_service: AuthService = Depends(get_auth_service)):
    token = credentials.credentials
    result = await auth_service.find_by_token(token)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return result


@router.get("/google/login")
async def google_login(request: Request, google_oauth: GoogleOAuthService = Depends(get_google_oauth_service)):
    # Initiate Google OAuth flow
    try:
        request.session.clear()
        return await google_oauth.get_authorization_url(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initiate Google login: {str(e)}")


@router.get("/google/callback")
async def google_callback(request: Request, google_oauth: GoogleOAuthService = Depends(get_google_oauth_service)):
    # Handle Google OAuth callback
    try:
        result = await google_oauth.handle_callback(request)
        user = result["user"]
        google_token = result["google_token"]
        
        expires_in = google_token.get("expires_in", 3600)
        access_token_expires = timedelta(seconds=expires_in)
        access_token = security_manager.create_access_token_from_google_user(user_id=str(user.id), email=user.email, expires_delta=access_token_expires)
        
        redirect_url = google_oauth.get_redirect_url(request)
        response = RedirectResponse(url=redirect_url)
        is_production = redirect_url.startswith("https://")
        
        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=is_production, samesite="lax", max_age=expires_in, path="/")
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google authentication failed: {str(e)}")


@router.get("/google/me")
async def google_user_info(access_token: Optional[str] = Cookie(None), google_oauth: GoogleOAuthService = Depends(get_google_oauth_service)):
    # Get user info from Google OAuth cookie
    try:
        user_data = security_manager.get_current_user_from_cookie(access_token)
        from app.repositories.users_repository import UsersRepository
        users_repo = UsersRepository()
        user = await users_repo.find_by_id(user_data["user_id"])
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_picture": user.profile_picture,
            "auth_provider": user.auth_provider,
            "is_verified": user.is_verified
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")


@router.post("/google/logout")
async def google_logout():
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie(key="access_token", path="/")
    return response
