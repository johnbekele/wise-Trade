#!/bin/bash
# Setup script for wise-Trade application
# Run this script to set up environment variables

export MONGO_URI="mongodb+srv://john:pass123@cluster0.yjky4oo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
export MONGO_DATABASE="wise_trade"
export MONGO_COLLECTION="users"
export MONGO_USERNAME="john"
export MONGO_PASSWORD="pass123"

echo "Environment variables set successfully!"
echo "MONGO_URI: $MONGO_URI"
echo "MONGO_DATABASE: $MONGO_DATABASE"

# Start the application
echo "Starting FastAPI application..."
source myenv/bin/activate
uvicorn app.main:app --reload
