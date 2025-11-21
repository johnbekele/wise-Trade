#!/bin/bash

# Start Vite dev server without proxy function interference

cd "$(dirname "$0")/frontend" || exit

echo "🚀 Starting Wise Trade Frontend (Node $(node --version))..."
echo ""
echo "📍 Opening: http://localhost:3000"
echo ""

# Unset npm/npx functions and run vite
unset -f npm 2>/dev/null
unset -f npx 2>/dev/null

# Run the dev server
exec command npm run dev

