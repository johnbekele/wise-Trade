# 🚀 Finnhub API Setup Guide

## Why Finnhub?

✅ **Better than Alpha Vantage:**
- Faster API responses
- More generous free tier (60 calls/minute vs 5 calls/minute)
- Real-time data
- Better company profiles
- Market news included
- WebSocket support for streaming

## 🔑 Get Your FREE Finnhub API Key

### Step 1: Sign Up (30 seconds)
1. Visit: https://finnhub.io/register
2. Enter your email
3. Create a password
4. Click "Sign Up"

### Step 2: Get Your API Key
1. After signing up, you'll be redirected to your dashboard
2. Your API key is displayed prominently at the top
3. Copy it (looks like: `cq1abc2defg3hijklm4nopqr`)

### Step 3: Add to .env File
```bash
# Open your .env file
nano .env

# Add this line:
FINNHUB_API_KEY=your_api_key_here
FINNHUB_API_URL=https://finnhub.io/api/v1

# Save and exit (Ctrl+X, then Y, then Enter)
```

## 📊 Finnhub Free Tier Limits

| Feature | Free Tier |
|---------|-----------|
| API Calls | 60 calls/minute |
| Real-time Data | ✅ Yes |
| Company Profiles | ✅ Yes |
| Market News | ✅ Yes |
| Historical Data | ✅ Yes |
| Technical Indicators | ✅ Yes |
| WebSocket | ✅ Yes |

## 🎯 API Endpoints We Use

1. **Stock Quote** - Real-time prices
   - `GET /quote?symbol=AAPL`

2. **Candles** - Historical OHLCV data for charts
   - `GET /stock/candle?symbol=AAPL&resolution=D`

3. **Company Profile** - Company information
   - `GET /stock/profile2?symbol=AAPL`

4. **Symbol Search** - Search for stocks
   - `GET /search?q=apple`

5. **Company News** - News for specific stocks
   - `GET /company-news?symbol=AAPL`

6. **Market News** - General market news
   - `GET /news?category=general`

## ✅ Verify Your Setup

After adding the key, restart the backend:

```bash
cd /home/johanan/wise-Trade
./start-backend.sh
```

Look for this in the startup logs:
```
✅ Finnhub API: ✓ Key present (length: 20)
```

## 🧪 Test the API

```bash
# Test getting a stock quote
curl "http://localhost:8000/api/stocks/quote/AAPL"

# Test search
curl "http://localhost:8000/api/stocks/search?keywords=apple"

# Test market movers
curl "http://localhost:8000/api/stocks/market-movers"
```

## 📚 Finnhub Documentation

- **Dashboard**: https://finnhub.io/dashboard
- **API Docs**: https://finnhub.io/docs/api
- **Status Page**: https://status.finnhub.io/

## 🆚 Comparison with Alpha Vantage

| Feature | Finnhub (Free) | Alpha Vantage (Free) |
|---------|----------------|----------------------|
| Rate Limit | 60/min | 5/min |
| Real-time | ✅ Yes | ❌ 15-min delay |
| Company Info | ✅ Rich data | ✅ Basic data |
| News | ✅ Included | ❌ Not included |
| Setup | Simple | Simple |
| WebSocket | ✅ Yes | ❌ No |

## 🎉 You're All Set!

Once your API key is added to `.env` and the backend is restarted, your app will use Finnhub for all stock data!

Visit http://localhost:3000 and enjoy faster, real-time stock data! 🚀
