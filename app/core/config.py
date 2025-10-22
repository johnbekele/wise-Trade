import os
from dotenv import load_dotenv
import pymongo

load_dotenv()

class Config:

    #  MongoDB configuration
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DATABASE = os.getenv("MONGO_DATABASE")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
    MONGO_USERNAME = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

    # SMTP configuration
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))  
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    # Secret key
    SECRET_KEY=os.getenv("SECRET_KEY")
    REFRESH_SECRET_KEY=os.getenv("REFRESH_SECRET_KEY")
    ALGORITHM=os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    TOKEN_EXPIRE_DAYS=int(os.getenv("TOKEN_EXPIRE_DAYS", 1))
    TOKEN_EXPIRE_MINUTES=int(os.getenv("TOKEN_EXPIRE_MINUTES", 15))


    # Backend URL
    FRONTEND_URL=os.getenv("FRONTEND_URL")


    # News API configuration
    NEWS_API_KEY=os.getenv("NEWS_API_KEY")
    NEWS_API_URL=os.getenv("NEWS_API_URL")
    







settings = Config()