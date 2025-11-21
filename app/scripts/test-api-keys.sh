#!/bin/bash

# Quick script to test all your API keys

echo "🔑 Testing API Keys..."
echo "================================"
echo ""

# Test Alpha Vantage
echo "1️⃣  Testing Alpha Vantage API..."
ALPHA_KEY=$(grep ALPHA_VANTAGE_API_KEY .env | cut -d '=' -f2)
if [ -z "$ALPHA_KEY" ]; then
    echo "   ❌ API key not found in .env"
else
    echo "   Key: ${ALPHA_KEY:0:10}..."
    RESPONSE=$(curl -k -s "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=$ALPHA_KEY")
    if echo "$RESPONSE" | grep -q "Error Message\|Invalid"; then
        echo "   ❌ Invalid API key!"
        echo "   Get new key: https://www.alphavantage.co/support/#api-key"
    elif echo "$RESPONSE" | grep -q "Global Quote"; then
        echo "   ✅ Working!"
    else
        echo "   ⚠️  Unknown response: $RESPONSE"
    fi
fi
echo ""

# Test News API
echo "2️⃣  Testing News API..."
NEWS_KEY=$(grep "^NEWS_API_KEY=" .env | cut -d '=' -f2)
if [ -z "$NEWS_KEY" ]; then
    echo "   ❌ API key not found in .env"
else
    echo "   Key: ${NEWS_KEY:0:10}..."
    RESPONSE=$(curl -k -s "https://newsapi.org/v2/top-headlines?country=us&apiKey=$NEWS_KEY&pageSize=1")
    if echo "$RESPONSE" | grep -q "apiKeyInvalid\|apiKeyMissing"; then
        echo "   ❌ Invalid API key!"
        echo "   Get new key: https://newsapi.org/register"
    elif echo "$RESPONSE" | grep -q '"status":"ok"'; then
        echo "   ✅ Working!"
    else
        echo "   ⚠️  Check: https://newsapi.org/register"
    fi
fi
echo ""

# Test Google Gemini
echo "3️⃣  Testing Google Gemini API..."
GEMINI_KEY=$(grep "^GOOGLE_API_KEY=" .env | cut -d '=' -f2)
if [ -z "$GEMINI_KEY" ]; then
    GEMINI_KEY=$(grep "^GEMINI_API_KEY=" .env | cut -d '=' -f2)
fi
if [ -z "$GEMINI_KEY" ]; then
    echo "   ❌ API key not found in .env"
    echo "   Get key: https://makersuite.google.com/app/apikey"
else
    echo "   Key: ${GEMINI_KEY:0:10}..."
    echo "   ℹ️  Testing via backend (can't test directly)"
fi
echo ""

# Test Frontend Logo API
echo "4️⃣  Checking Frontend Logo API..."
if [ -f "frontend/.env" ]; then
    LOGO_KEY=$(grep VITE_LOGO_API_KEY frontend/.env | cut -d '=' -f2)
    if [ -z "$LOGO_KEY" ]; then
        echo "   ❌ VITE_LOGO_API_KEY not found in frontend/.env"
    else
        echo "   ✅ Key found: ${LOGO_KEY:0:10}..."
    fi
else
    echo "   ❌ frontend/.env file not found"
    echo "   Create: echo 'VITE_LOGO_API_KEY=your_key' > frontend/.env"
fi
echo ""

echo "================================"
echo "📋 Summary:"
echo ""
echo "Backend API keys go in:  .env"
echo "Frontend keys go in:     frontend/.env"
echo ""
echo "🔗 Get API Keys:"
echo "• Alpha Vantage: https://www.alphavantage.co/support/#api-key"
echo "• News API:      https://newsapi.org/register"
echo "• Google Gemini: https://makersuite.google.com/app/apikey"
echo "• Brandfetch:    https://brandfetch.com/"
echo ""

