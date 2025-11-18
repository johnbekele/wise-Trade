# Wise Trade - Complete Setup Guide

## 🎯 Project Overview

A modern stock trading platform with real-time data from Alpha Vantage API and AI-powered news analysis using Google Gemini.

### Backend (FastAPI + Python)
- Stock market data from Alpha Vantage
- AI news analysis with Google Gemini
- User authentication
- MongoDB database

### Frontend (React + Vite + Tailwind)
- Real-time stock dashboard
- Interactive price charts
- AI news analysis
- Responsive design

---

## 📦 Installation

### Backend Setup

1. **Activate virtual environment:**
```bash
cd /home/johanan/wise-Trade
source myenv/bin/activate
```

2. **Install backend dependencies (if not already installed):**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables (.env file):**
```env
# MongoDB
MONGO_URI=your_mongodb_uri
MONGO_DATABASE=wise_trade
MONGO_USERNAME=your_username
MONGO_PASSWORD=your_password

# APIs
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
ALPHA_VANTAGE_API_URL=https://www.alphavantage.co/query
NEWS_API_KEY=your_news_api_key
NEWS_API_URL=https://newsapi.org/v2
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-pro

# Auth
SECRET_KEY=your_secret_key
REFRESH_SECRET_KEY=your_refresh_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# SMTP (for email)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Frontend
FRONTEND_URL=http://localhost:3000
```

4. **Start the backend server:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend API will be available at: `http://localhost:8000`

---

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd /home/johanan/wise-Trade/frontend
```

2. **Install dependencies:**
```bash
npm install
```

If npm install fails, install packages individually:
```bash
npm install react@^18.3.1 react-dom@^18.3.1
npm install react-router-dom@^6.23.1
npm install axios@^1.7.2
npm install recharts@^2.12.7
npm install lucide-react@^0.379.0
npm install --save-dev vite@^5.3.1
npm install --save-dev @vitejs/plugin-react@^4.3.1
npm install --save-dev tailwindcss@^3.4.4
npm install --save-dev postcss@^8.4.38
npm install --save-dev autoprefixer@^10.4.19
```

3. **Start the development server:**
```bash
npm run dev
```

The frontend will be available at: `http://localhost:3000`

---

## 🚀 API Endpoints

### Stock Endpoints (`/api/stocks`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/quote/{symbol}` | Get real-time stock quote |
| GET | `/intraday/{symbol}` | Get intraday price data (1min-60min intervals) |
| GET | `/daily/{symbol}` | Get daily historical data |
| GET | `/weekly/{symbol}` | Get weekly historical data |
| GET | `/search?keywords=QUERY` | Search for stock symbols |
| GET | `/overview/{symbol}` | Get company fundamentals |
| GET | `/market-movers` | Get top gainers/losers/most active |
| GET | `/market-status` | Get current market status |
| POST | `/quotes/batch` | Get quotes for multiple symbols |

### AI News Endpoints (`/api/ai`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analyze-news?query=QUERY` | Analyze news for a specific query |
| GET | `/analyze-news/{query}` | Analyze news (path param) |
| POST | `/analyze-news` | Analyze news (JSON body) |
| GET | `/market-impact?limit=10` | Get top market-impacting news |

### Example API Calls

**Get stock quote:**
```bash
curl http://localhost:8000/api/stocks/quote/AAPL
```

**Search stocks:**
```bash
curl "http://localhost:8000/api/stocks/search?keywords=tesla"
```

**Get market impact news:**
```bash
curl "http://localhost:8000/api/ai/market-impact?limit=10"
```

**Analyze specific news:**
```bash
curl "http://localhost:8000/api/ai/analyze-news?query=nvidia"
```

---

## 🎨 Frontend Features

### Dashboard (`/`)
- Customizable stock watchlist
- Real-time price updates (30-second refresh)
- Market movers (gainers, losers, most active)
- Stock search with autocomplete
- Click cards to view detailed information

### Stock Detail (`/stock/{symbol}`)
- Real-time price and metrics
- Interactive price charts (1min, 5min, 15min, 30min, 60min intervals)
- Company overview and fundamentals
- Key statistics (P/E ratio, market cap, 52-week high/low)

### News Analysis (`/news`)
- AI-powered market impact news analysis
- Custom news search and analysis
- Actionable trading insights
- Sector and company impact assessment

---

## 🔧 Configuration

### Backend Configuration

File: `app/core/config.py`

All configuration is loaded from environment variables using `python-dotenv`.

### Frontend Configuration

File: `frontend/vite.config.js`

```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

---

## 🎯 Key Features

### Backend Features
✅ Alpha Vantage API integration for real-time stock data  
✅ Google Gemini AI for news analysis  
✅ News API integration for financial news  
✅ FastAPI with async support  
✅ MongoDB with Beanie ODM  
✅ JWT authentication  
✅ Startup checks for API connectivity  
✅ SSL error handling for WSL environments  

### Frontend Features
✅ Modern React 18 with hooks  
✅ Vite for fast development  
✅ Tailwind CSS for styling  
✅ React Router for navigation  
✅ Recharts for data visualization  
✅ Responsive mobile-first design  
✅ Real-time data updates  
✅ Stock search with autocomplete  
✅ Interactive charts  

---

## 📊 Data Flow

1. **User requests stock data** → Frontend sends API request
2. **Backend receives request** → Calls Alpha Vantage API
3. **Alpha Vantage returns data** → Backend processes and formats
4. **Backend sends response** → Frontend displays in UI
5. **Auto-refresh** → Frontend polls for updates every 30 seconds

For AI news analysis:
1. **User queries news** → Frontend sends query to backend
2. **Backend fetches news** → Calls News API
3. **Backend sends to AI** → Google Gemini analyzes
4. **AI returns analysis** → Backend formats response
5. **Frontend displays** → Shows insights and recommendations

---

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
# Or use a different port
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**SSL certificate errors (WSL):**
The backend has built-in SSL error handling. If you still see issues:
```bash
sudo apt-get update && sudo apt-get install ca-certificates
```

**Import errors:**
```bash
source myenv/bin/activate
pip install -r requirements.txt
```

### Frontend Issues

**npm install fails:**
Try clearing cache:
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**Port 3000 in use:**
Change port in `vite.config.js` or kill the process:
```bash
lsof -ti:3000 | xargs kill -9
```

**API connection errors:**
Make sure backend is running on `http://localhost:8000`

---

## 📚 Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **MongoDB**: NoSQL database
- **Beanie**: Async ODM for MongoDB
- **Alpha Vantage**: Stock market data
- **Google Gemini**: AI analysis
- **News API**: Financial news

### Frontend
- **React 18**: UI library
- **Vite**: Build tool
- **Tailwind CSS**: Utility-first CSS
- **React Router**: Routing
- **Recharts**: Charts
- **Axios**: HTTP client
- **Lucide React**: Icons

---

## 🚦 Running Both Servers

**Terminal 1 - Backend:**
```bash
cd /home/johanan/wise-Trade
source myenv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd /home/johanan/wise-Trade/frontend
npm run dev
```

Then open your browser to: `http://localhost:3000`

---

## 📝 Next Steps

1. **Get API Keys:**
   - Alpha Vantage: https://www.alphavantage.co/support/#api-key
   - News API: https://newsapi.org/register
   - Google Gemini: https://makersuite.google.com/app/apikey

2. **Configure .env file** with your API keys

3. **Start both servers** (backend and frontend)

4. **Add stocks to watchlist** on the dashboard

5. **Explore AI news analysis** on the news page

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Alpha Vantage API](https://www.alphavantage.co/documentation/)
- [Recharts](https://recharts.org/)

---

## 📄 License

MIT License - Free for personal and commercial use.

