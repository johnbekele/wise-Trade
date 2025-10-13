#!/usr/bin/env python3
"""
Test script for wise-Trade API
Run this to test the user creation endpoint
"""

import requests
import json

# Test data
test_user = {
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "password123"
}

# API endpoint
url = "http://127.0.0.1:8000/api/test/user"

print("🧪 Testing wise-Trade API...")
print(f"📡 Endpoint: {url}")
print(f"📝 Test data: {json.dumps(test_user, indent=2)}")

try:
    # Test user creation
    print("\n1️⃣ Testing user creation...")
    response = requests.post(url, json=test_user)
    
    if response.status_code == 200:
        print("✅ User created successfully!")
        print(f"📄 Response: {response.json()}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"📄 Response: {response.text}")
    
    # Test user retrieval
    print("\n2️⃣ Testing user retrieval...")
    get_response = requests.get(url)
    
    if get_response.status_code == 200:
        print("✅ Users retrieved successfully!")
        print(f"📄 Response: {get_response.json()}")
    else:
        print(f"❌ Error: {get_response.status_code}")
        print(f"📄 Response: {get_response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Connection failed! Make sure the FastAPI server is running.")
    print("💡 Run: ./start_app.sh")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print("\n🏁 Test completed!")
