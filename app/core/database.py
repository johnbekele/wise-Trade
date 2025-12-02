from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import certifi

#collection models
from app.models.users import User
from app.models.auth import AuthToken

MONGO_URI = settings.MONGO_URI
MONGO_DATABASE = settings.MONGO_DATABASE


if not MONGO_URI:
    raise ValueError("MONGO_URI is not set")
if not MONGO_DATABASE:
    raise ValueError("MONGO_DATABASE is not set")


client=None

async def init_database():
    """Initialize Beanie"""
    print("Initializing Beanie...")
    global client
    try:
            # Try with SSL configuration first
            # Increased timeouts for cloud environments (30 seconds)
            # Added connection pooling for better performance
            try:
                client = AsyncIOMotorClient(
                    MONGO_URI, 
                    tlsCAFile=certifi.where(),
                    tlsAllowInvalidCertificates=True,
                    tlsAllowInvalidHostnames=True,
                    serverSelectionTimeoutMS=30000,  # 30 seconds for cloud
                    connectTimeoutMS=30000,  # 30 seconds for cloud
                    socketTimeoutMS=30000,  # 30 seconds socket timeout
                    maxPoolSize=50,  # Connection pool size
                    minPoolSize=10,  # Minimum connections
                    maxIdleTimeMS=45000,  # Close idle connections after 45s
                    retryWrites=True,  # Retry writes on network errors
                    retryReads=True,  # Retry reads on network errors
                )
                database = client[MONGO_DATABASE]
                print("MongoDB client initialized successfully 🍃 MongoDB URI: ", MONGO_URI)
            except Exception as ssl_error:
                print(f"SSL connection failed, trying alternative method: {ssl_error}")
                # Fallback: try without SSL verification with cloud-optimized settings
                client = AsyncIOMotorClient(
                    MONGO_URI,
                    tlsAllowInvalidCertificates=True,
                    tlsAllowInvalidHostnames=True,
                    serverSelectionTimeoutMS=30000,  # 30 seconds for cloud
                    connectTimeoutMS=30000,  # 30 seconds for cloud
                    socketTimeoutMS=30000,  # 30 seconds socket timeout
                    maxPoolSize=50,  # Connection pool size
                    minPoolSize=10,  # Minimum connections
                    maxIdleTimeMS=45000,  # Close idle connections after 45s
                    retryWrites=True,  # Retry writes on network errors
                    retryReads=True,  # Retry reads on network errors
                )
                database = client[MONGO_DATABASE]
                print("MongoDB client initialized with fallback method 🍃 MongoDB URI: ", MONGO_URI)
    except Exception as e:
        print("Error initializing MongoDB client: ", e)
        raise e
    try:
        await init_beanie(database=database, document_models=[User , AuthToken], allow_index_dropping=False, recreate_views=False)
        print("Beanie initialized successfully 🍃")
    except Exception as e:
        print("Error initializing Beanie: ", e)
        raise e


async def close_db_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("MongoDB connection closed successfully 🍃")