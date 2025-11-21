#!/bin/bash

echo "🔑 Finnhub API Key Setup"
echo "========================"
echo ""
echo "Step 1: Open your browser and go to:"
echo "👉 https://finnhub.io/register"
echo ""
echo "Step 2: Sign up (30 seconds)"
echo "  - Enter your email"
echo "  - Create a password"
echo "  - Click 'Sign Up'"
echo ""
echo "Step 3: Get your API key"
echo "  - After signup, you'll see your API key on the dashboard"
echo "  - It looks like: cq1abc2defg3hijklm4nopqr"
echo ""
echo "Step 4: Enter your API key below"
echo ""
read -p "Enter your Finnhub API key: " API_KEY

if [ -z "$API_KEY" ]; then
    echo "❌ No key entered. Exiting..."
    exit 1
fi

# Update .env file
cd /home/johanan/wise-Trade
sed -i "s/^FINNHUB_API_KEY=.*/FINNHUB_API_KEY=$API_KEY/" .env

echo ""
echo "✅ API key saved to .env!"
echo ""
echo "Testing key..."
curl -s "https://finnhub.io/api/v1/quote?symbol=AAPL&token=$API_KEY" | head -5

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Key is valid! Restarting backend..."
    pkill -9 uvicorn
    sleep 2
    cd /home/johanan/wise-Trade
    source myenv/bin/activate
    nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
    echo "✅ Backend restarted!"
    echo "✅ Visit http://localhost:3000 to see your app with real-time stock data!"
else
    echo "❌ Key validation failed. Please check your key and try again."
fi

