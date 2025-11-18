from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import test
from app.core.database import init_database, close_db_connection
from app.core.startup_checks import run_startup_checks
from contextlib import asynccontextmanager


#routers
from app.routers import users
from app.routers import auth
from app.routers import ai
from app.routers import stocks

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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test.router , tags=["test"] , prefix="/api/test")
app.include_router(users.router , tags=["users"] , prefix="/api/users")
app.include_router(auth.router , tags=["auth"] , prefix="/api/auth")
app.include_router(ai.router , tags=["ai"] , prefix="/api/ai")
app.include_router(stocks.router , tags=["stocks"] , prefix="/api/stocks")