#!/bin/bash
# Setup script for wise-Trade application
# IMPORTANT: Set your environment variables before running this script!

# Check if environment variables are set
if [ -z "$MONGO_URI" ]; then
    echo "❌ ERROR: MONGO_URI environment variable is not set!"
    echo "Please set your MongoDB connection string:"
    echo "export MONGO_URI='your_mongodb_connection_string'"
    echo "export MONGO_DATABASE='your_database_name'"
    exit 1
fi

if [ -z "$MONGO_DATABASE" ]; then
    echo "❌ ERROR: MONGO_DATABASE environment variable is not set!"
    echo "Please set your database name:"
    echo "export MONGO_DATABASE='your_database_name'"
    exit 1
fi

echo "✅ Environment variables are set!"
echo "📊 Database: $MONGO_DATABASE"

# Start the application
echo "🚀 Starting FastAPI application..."
source myenv/bin/activate
uvicorn app.main:app --reload
