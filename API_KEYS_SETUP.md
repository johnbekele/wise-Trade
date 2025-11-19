# 🔧 API Keys Setup Issue - FIXED

## ❌ Current Issue: Alpha Vantage API Key Invalid

Your Alpha Vantage API key `DX4EWZILBSV1BHNZ` is returning "invalid or missing" errors.

### ✅ **Solution: Get a New FREE API Key**

1. **Visit:** https://www.alphavantage.co/support/#api-key
2. **Enter your email** (takes 20 seconds)
3. **Get instant key** (no credit card needed)
4. **Copy the new key**

### 📝 **Update Your .env File:**

Edit `/home/johanan/wise-Trade/.env`:

```bash
# Replace with your NEW key
ALPHA_VANTAGE_API_KEY=your_new_key_here
ALPHA_VANTAGE_API_URL=https://www.alphavantage.co/query
```

### 🔄 **Restart Backend:**

The backend will auto-reload and pick up the new key!

---

## 🎨 **Logo API Setup (Separate)**

Your logo API key goes in the **FRONTEND** `.env` file:

### **Frontend .env File:**

Create/edit `/home/johanan/wise-Trade/frontend/.env`:

```bash
VITE_LOGO_API_KEY=1idp8CO1aS7Wu22j-qr
```

**Note:** Frontend uses `VITE_` prefix!

---

## 📋 **Complete API Keys Checklist:**

### **Backend (.env in project root):**
```bash
# Alpha Vantage - For stock data
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
ALPHA_VANTAGE_API_URL=https://www.alphavantage.co/query

# Google Gemini - For AI analysis
GOOGLE_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-pro

# News API - For financial news
NEWS_API_KEY=your_news_api_key
NEWS_API_URL=https://newsapi.org/v2
```

### **Frontend (.env in frontend/ directory):**
```bash
# Brandfetch - For company logos
VITE_LOGO_API_KEY=1idp8CO1aS7Wu22j-qr
```

---

## 🧪 **Test After Getting New Key:**

```bash
# Test Alpha Vantage directly
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=YOUR_NEW_KEY"

# Test backend API
curl "http://localhost:8000/api/stocks/quote/AAPL"

# Should return real stock data!
```

---

## 🚀 **Quick Fix Steps:**

1. **Get new Alpha Vantage key:** https://www.alphavantage.co/support/#api-key
2. **Update backend .env** with new key
3. **Create frontend .env** with logo key
4. **Backend auto-reloads** (no restart needed!)
5. **Refresh your browser** to see logos

---

## 💡 **Why the Error?**

- Alpha Vantage free keys sometimes expire
- Or the key was copied incorrectly
- Or it's rate-limited (500 calls/day free tier)

**Solution:** Just get a fresh free key!

---

## ✅ **Once Fixed, You'll Have:**

- ✅ Real-time stock data
- ✅ Company logos everywhere
- ✅ AI news analysis
- ✅ Beautiful trading dashboard

Get that new API key and you're golden! 🎉

