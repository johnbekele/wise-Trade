#!/bin/bash

# Simple script to run frontend dev server without proxy issues

cd "$(dirname "$0")/frontend" || exit

echo "🚀 Starting Wise Trade Frontend..."
echo ""
echo "Opening: http://localhost:3000"
echo ""

# Run vite directly with npx to avoid shell function conflicts
exec npx vite --host 0.0.0.0 --port 3000

