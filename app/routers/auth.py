from app.schemas.user_schema import UserRead
from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from app.services.auth_service import AuthService
from app.schemas.auth_schema import LoginResponse, LoginRequest
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials

router = APIRouter()
bearer_scheme = HTTPBearer()
def get_auth_service() -> AuthService:
    return AuthService()



@router.post("/login")
async def login(login_request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)) -> LoginResponse:
    print(f"user input from route : username {login_request.username}  password:{login_request.password}")
    return await auth_service.login(login_request.username, login_request.password)


@router.post("/resend-email-verification/{user_id}")
async def send_email_verification(
    user_id, 
    background_tasks: BackgroundTasks,
    auth_service: AuthService = Depends(get_auth_service)
) -> str:
    return await auth_service.send_email_verification(user_id, background_tasks)


@router.get("/verify-email")
async def verify_email(token: str = Query(...), auth_service: AuthService = Depends(get_auth_service)):
    """Verify email with proper error handling"""
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
        # Generic error
        raise HTTPException(status_code=500, detail=result or "Error verifying email")

@router.get("/me")
async def user_info(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), auth_service: AuthService = Depends(get_auth_service)) :
    token = credentials.credentials
    result = await auth_service.find_by_token(token)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return result

