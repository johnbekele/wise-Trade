#!/bin/bash
# 🔒 CREDENTIAL ROTATION SCRIPT
# This script helps rotate credentials after a security incident

echo "🔒 CREDENTIAL ROTATION SCRIPT"
echo "=============================="
echo ""

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "⚠️  IMPORTANT: This script helps you rotate credentials after a security incident"
echo ""

# MongoDB Atlas credentials rotation
echo "1. 🔄 MONGODB ATLAS CREDENTIALS ROTATION"
echo "   - Go to MongoDB Atlas Dashboard"
echo "   - Navigate to Database Access"
echo "   - Create a new user with a strong password"
echo "   - Delete the old user"
echo "   - Update your .env file with new credentials"
echo ""

# Generate new secret keys
echo "2. 🔑 GENERATING NEW SECRET KEYS"
echo "   Generating new JWT secret keys..."

SECRET_KEY=$(openssl rand -hex 32)
REFRESH_SECRET_KEY=$(openssl rand -hex 32)

echo "   New SECRET_KEY: $SECRET_KEY"
echo "   New REFRESH_SECRET_KEY: $REFRESH_SECRET_KEY"
echo ""

# Update .env file if it exists
if [ -f ".env" ]; then
    echo "3. 📝 UPDATING .env FILE"
    echo "   Updating .env file with new secret keys..."
    
    # Backup current .env
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
    echo "   ✅ Backup created: .env.backup.$(date +%Y%m%d_%H%M%S)"
    
    # Update secret keys
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    sed -i "s/REFRESH_SECRET_KEY=.*/REFRESH_SECRET_KEY=$REFRESH_SECRET_KEY/" .env
    
    echo "   ✅ .env file updated with new secret keys"
else
    echo "3. 📝 .env FILE NOT FOUND"
    echo "   Please create a .env file with the new credentials"
fi

echo ""
echo "4. 🚀 NEXT STEPS"
echo "   - Update MongoDB Atlas connection string in .env"
echo "   - Restart your application"
echo "   - Test all functionality"
echo "   - Monitor for any unauthorized access"
echo ""

echo "5. 🔍 SECURITY CHECKLIST"
echo "   - [ ] MongoDB Atlas password rotated"
echo "   - [ ] JWT secret keys updated"
echo "   - [ ] Application restarted"
echo "   - [ ] All tests passing"
echo "   - [ ] No unauthorized access detected"
echo ""

echo "✅ Credential rotation script completed!"
echo "⚠️  Remember to update your production environment as well!"
