#!/bin/bash

# Start the Wise Trade Backend

cd "$(dirname "$0")" || exit

echo "🚀 Starting Wise Trade Backend..."
echo ""

# Activate virtual environment
if [ -f "myenv/bin/activate" ]; then
    source myenv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Warning: Virtual environment not found"
fi

echo ""
echo "📍 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

