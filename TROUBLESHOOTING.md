# 🔧 Troubleshooting Guide - Frontend Not Loading Data

## ✅ **ISSUE FIXED: CORS Configuration Added**

The backend wasn't allowing requests from the frontend. I've added CORS middleware to `app/main.py`.

---

## 🚀 **To Start the App Properly:**

### **Terminal 1 - Start Backend:**
```bash
cd /home/johanan/wise-Trade
./start-backend.sh
```

### **Terminal 2 - Start Frontend:**
```bash
cd /home/johanan/wise-Trade
./start-frontend.sh
```

---

## ✅ **What I Fixed:**

1. **Added CORS middleware** to allow frontend requests
2. **Created start scripts** for easy server management

---

## 🔍 **Check if Backend is Running:**

```bash
# Check if backend is running
curl http://localhost:8000/api/stocks/quote/AAPL

# Should return JSON data, not an error
```

---

## 📝 **Important: API Keys Required**

Make sure your `.env` file has these keys:

```env
# Alpha Vantage (for stock data)
ALPHA_VANTAGE_API_KEY=your_key_here

# Google Gemini (for AI analysis)
GOOGLE_API_KEY=your_key_here

# News API (for financial news)
NEWS_API_KEY=your_key_here
```

**Get free API keys:**
- Alpha Vantage: https://www.alphavantage.co/support/#api-key
- Google Gemini: https://makersuite.google.com/app/apikey
- News API: https://newsapi.org/register

---

## 🐛 **Common Issues & Solutions:**

### 1. **Frontend shows "Loading..." forever**
**Cause:** Backend not running or CORS issue  
**Fix:** 
- Restart backend: `./start-backend.sh`
- Check browser console (F12) for errors

### 2. **"Network Error" in browser console**
**Cause:** Backend not accessible  
**Fix:**
```bash
# Check if backend is running
curl http://localhost:8000/api/test/

# Should return: {"message":"Test route is working"}
```

### 3. **API returns errors about missing keys**
**Cause:** Missing API keys in `.env` file  
**Fix:**
- Create/edit `.env` file in project root
- Add your API keys (see above)
- Restart backend

### 4. **Stock data not loading**
**Cause:** Invalid or missing Alpha Vantage API key  
**Fix:**
- Test the API key:
```bash
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=YOUR_KEY"
```
- Should return stock data, not error message

### 5. **AI news analysis not working**
**Cause:** Missing or invalid Google Gemini API key  
**Fix:**
- Check backend logs for error messages
- Verify `GOOGLE_API_KEY` in `.env` file
- Restart backend after adding key

### 6. **CORS errors in browser console**
**Cause:** Already fixed! But if you see CORS errors:  
**Fix:** Make sure backend has CORS middleware (already added)

---

## 🧪 **Testing Your Setup:**

### **1. Test Backend Directly:**
```bash
# Test stocks API
curl http://localhost:8000/api/stocks/quote/AAPL

# Test AI news API  
curl "http://localhost:8000/api/ai/market-impact?limit=5"

# Test market movers
curl http://localhost:8000/api/stocks/market-movers
```

### **2. Check Browser Console:**
- Open browser DevTools (F12)
- Go to Console tab
- Look for red errors
- Common errors:
  - "CORS" → Backend not running or CORS not configured
  - "Network Error" → Backend not accessible
  - "404" → Wrong API endpoint
  - "500" → Backend error (check backend logs)

### **3. Check Backend Logs:**
Look at the terminal where backend is running for:
- Startup errors
- API key warnings
- Request errors

---

## 📊 **Expected Behavior:**

### **Dashboard (`http://localhost:3000`):**
- Shows 5 default stocks (AAPL, GOOGL, MSFT, TSLA, AMZN)
- Real-time prices update
- Market movers section (top gainers, losers, most active)
- Search bar to add more stocks

### **Stock Detail Page:**
- Click any stock card
- Shows detailed information
- Interactive price chart
- Company overview

### **News Analysis Page:**
- Top market-impact news (AI-analyzed)
- Custom news search
- Trading insights

---

## 🔑 **Quick Checklist:**

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] `.env` file has API keys
- [ ] CORS configured (✅ already done)
- [ ] Browser console shows no errors
- [ ] Can access http://localhost:8000/docs

---

## 🆘 **Still Having Issues?**

1. **Restart both servers**
2. **Check browser console for specific errors**
3. **Check backend terminal for error messages**
4. **Verify API keys are valid**
5. **Test backend APIs directly with curl**

---

## ✅ **Success Indicators:**

You'll know it's working when:
- Dashboard loads with stock cards
- Prices show real data (not $0.00)
- Market movers section shows data
- Search works and finds stocks
- AI news analysis returns insights
- No red errors in browser console

---

**The CORS issue is now fixed! Restart your backend and it should work!** 🎉

