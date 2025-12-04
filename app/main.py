from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.routers import test
from app.core.database import init_database, close_db_connection
from app.core.startup_checks import run_startup_checks
from app.core.config import settings
from contextlib import asynccontextmanager


#routers
from app.routers import users
from app.routers import auth
from app.routers import ai
from app.routers import stocks
from app.routers import admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting lifespan...")
    
    # Run startup checks for API keys and endpoint connectivity
    run_startup_checks()
    
    # Initialize database
    await init_database()
    print("Beanie initialized successfully 🍃")
    
    yield
    
    print("Closing lifespan...")
    await close_db_connection()
    print("MongoDB connection closed successfully 🍃")

app = FastAPI(lifespan=lifespan)

# Add Session middleware (required for Google OAuth)
# Session middleware stores temporary data during OAuth flow
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY or "your-secret-key-change-in-production",
    max_age=3600,  # Session expires in 1 hour
    same_site="lax"  # CSRF protection
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000","https://wise-trade-client.vercel.app"],
    allow_credentials=True,  # Required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test.router , tags=["test"] , prefix="/api/test")
app.include_router(users.router , tags=["users"] , prefix="/api/users")
app.include_router(auth.router , tags=["auth"] , prefix="/api/auth")
app.include_router(ai.router , tags=["ai"] , prefix="/api/ai")
app.include_router(stocks.router , tags=["stocks"] , prefix="/api/stocks")
app.include_router(admin.router , tags=["admin"] , prefix="/api/admin")