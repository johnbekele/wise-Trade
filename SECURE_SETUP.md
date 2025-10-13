# 🔐 SECURE SETUP GUIDE

## ⚠️ IMPORTANT SECURITY NOTICE
**NEVER commit credentials or sensitive information to version control!**

## 🚀 Quick Start (Secure Method)

### 1. Set Environment Variables
```bash
# Set your MongoDB connection details
export MONGO_URI="your_mongodb_connection_string"
export MONGO_DATABASE="your_database_name"

# Verify they're set
echo $MONGO_URI
echo $MONGO_DATABASE
```

### 2. Start the Application
```bash
# Option 1: Use the startup script
./start_app.sh

# Option 2: Start manually
source myenv/bin/activate
uvicorn app.main:app --reload
```

### 3. Test the API
```bash
python test_api.py
```

## 🔧 Alternative: Using .env File

### 1. Create .env file
```bash
# Copy the template
cp env.template .env

# Edit with your actual values
nano .env
```

### 2. Install python-dotenv (if not already installed)
```bash
pip install python-dotenv
```

## 🛡️ Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** for sensitive data
3. **Rotate credentials** regularly
4. **Use MongoDB Atlas IP whitelist** for additional security
5. **Enable MongoDB Atlas audit logs** for monitoring

## 🆘 If Credentials Are Compromised

1. **Immediately rotate** the MongoDB Atlas password
2. **Revoke** the compromised credentials
3. **Check audit logs** for unauthorized access
4. **Update** all applications using the old credentials
5. **Review** git history and remove sensitive data

## 📝 Example API Usage

### Create User
```bash
curl -X POST "http://localhost:8000/api/test/user" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Get All Users
```bash
curl -X GET "http://localhost:8000/api/test/user"
```
