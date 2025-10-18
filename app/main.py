from fastapi import FastAPI
from app.routers import test
from app.core.database import init_database, close_db_connection
from contextlib import asynccontextmanager


#routers
from app.routers import users
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting lifespan...")
    await init_database()
    print("Beanie initialized successfully 🍃")
    yield
    print("Closing lifespan...")
    await close_db_connection()
    print("MongoDB connection closed successfully 🍃")

app = FastAPI(lifespan=lifespan)


app.include_router(test.router , tags=["test"] , prefix="/api/test")
app.include_router(users.router , tags=["users"] , prefix="/api/users")
app.include_router(auth.router , tags=["auth"] , prefix="/api/auth")
