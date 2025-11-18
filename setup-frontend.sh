#!/bin/bash

# Wise Trade Frontend Setup Script

echo "🚀 Setting up Wise Trade Frontend..."
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/frontend" || exit

echo "📦 Installing dependencies..."
echo ""

# Check if node_modules exists
if [ -d "node_modules" ]; then
    echo "⚠️  node_modules already exists. Cleaning up..."
    rm -rf node_modules package-lock.json
fi

# Install dependencies
echo "Installing React and React DOM..."
npm install react@^18.3.1 react-dom@^18.3.1

echo "Installing routing and HTTP client..."
npm install react-router-dom@^6.23.1 axios@^1.7.2

echo "Installing charts and icons..."
npm install recharts@^2.12.7 lucide-react@^0.379.0

echo "Installing build tools..."
npm install --save-dev vite@^5.3.1 @vitejs/plugin-react@^4.3.1

echo "Installing Tailwind CSS..."
npm install --save-dev tailwindcss@^3.4.4 postcss@^8.4.38 autoprefixer@^10.4.19

echo ""
echo "✅ Installation complete!"
echo ""
echo "To start the development server, run:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "The frontend will be available at: http://localhost:3000"

