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
    """Initialize Beanie with retry logic for network issues"""
    print("Initializing Beanie...")
    global client
    
    import asyncio
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            # Try with SSL configuration first
            # Increased timeouts for cloud environments (30 seconds)
            # Added connection pooling for better performance
            try:
                print(f"Attempt {attempt + 1}/{max_retries}: Connecting to MongoDB...")
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
                
                # Test the connection
                await asyncio.wait_for(client.admin.command('ping'), timeout=10.0)
                print("MongoDB client initialized successfully 🍃 MongoDB URI: ", MONGO_URI)
                break  # Success, exit retry loop
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
                
                # Test the connection
                await asyncio.wait_for(client.admin.command('ping'), timeout=10.0)
                print("MongoDB client initialized with fallback method 🍃 MongoDB URI: ", MONGO_URI)
                break  # Success, exit retry loop
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"❌ Connection attempt {attempt + 1} failed: {str(e)}")
                print(f"⏳ Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                print(f"❌ All {max_retries} connection attempts failed")
                print(f"Error: {str(e)}")
                print("\n💡 Troubleshooting tips:")
                print("   1. Check your internet connection")
                print("   2. Verify MONGO_URI in your .env file")
                print("   3. Check MongoDB Atlas IP whitelist (should allow 0.0.0.0/0 for Docker)")
                print("   4. In WSL2, try: sudo service docker restart")
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