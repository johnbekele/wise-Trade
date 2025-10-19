from app.schemas.user_schema import UserRead
from fastapi import APIRouter, Depends, Query, HTTPException
from app.services.auth_service import AuthService
from app.schemas.auth_schema import LoginResponse, LoginRequest

router = APIRouter()

def get_auth_service() -> AuthService:
    return AuthService()



@router.post("/login")
async def login(login_request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)) -> LoginResponse:
    print(f"user input from route : username {login_request.username}  password:{login_request.password}")
    return await auth_service.login(login_request.username, login_request.password)


@router.post("/resend-email-verification/{user_id}")
async def send_email_verification(user_id, auth_service: AuthService = Depends(get_auth_service)) -> str:
    return await auth_service.send_email_verification(user_id)


@router.get("/verify-email")
async def verify_email(token: str = Query(...), auth_service: AuthService = Depends(get_auth_service)) -> str:
    return await auth_service.verify_email(token)

@router.get("/me")
async def user_info(token: str = Query(...), auth_service: AuthService = Depends(get_auth_service)) -> UserRead:
    result = await auth_service.find_by_token(token)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return result