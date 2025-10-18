from fastapi import APIRouter , Depends
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