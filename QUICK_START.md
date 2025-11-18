# 🚀 Quick Start Guide - Wise Trade

## ✅ Your System Status
- ✅ Backend installed and working
- ✅ Frontend dependencies installed 
- ⚠️ Proxy configuration issue detected (workaround provided)

---

## 🎯 Running the Application

### Method 1: Use the Helper Scripts (Recommended)

**Terminal 1 - Backend:**
```bash
cd /home/johanan/wise-Trade
source myenv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd /home/johanan/wise-Trade
./run-frontend.sh
```

Then open your browser to: **http://localhost:3000**

---

### Method 2: Direct npx Command (Alternative)

If the script doesn't work, use this directly:

**Terminal 2 - Frontend:**
```bash
cd /home/johanan/wise-Trade/frontend
npx vite --host 0.0.0.0 --port 3000
```

---

## 🐛 Fixing the Proxy Issue (Optional)

The `http_proxy=: command not found` error is caused by npm/npx wrapper functions in your `.bashrc`.

**Temporary fix (current session only):**
```bash
unalias npm 2>/dev/null
unalias npx 2>/dev/null
unset -f npm 2>/dev/null
unset -f npx 2>/dev/null
```

**Permanent fix:**
Edit `~/.bashrc` and comment out or remove these lines:
```bash
# npm/npx functions to bypass proxy (proxy server not accessible)
    command http_proxy="" https_proxy="" npm "$@"
    command http_proxy="" https_proxy="" npx "$@"
```

Then restart your terminal or run: `source ~/.bashrc`

---

## ⚠️ Node Version Warning

Your Node version is v16.20.2, but Vite recommends v18+. 

**It should still work**, but if you encounter issues:

**Install Node 18+ using nvm:**
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18
```

Then reinstall frontend dependencies:
```bash
cd /home/johanan/wise-Trade/frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 What's Available

### Backend API (Port 8000)
- Stock quotes and data: http://localhost:8000/api/stocks/
- AI news analysis: http://localhost:8000/api/ai/
- API docs: http://localhost:8000/docs

### Frontend (Port 3000)
- Dashboard: http://localhost:3000/
- Stock details: http://localhost:3000/stock/AAPL
- News analysis: http://localhost:3000/news

---

## 🎮 Quick Test

**Test Backend:**
```bash
curl http://localhost:8000/api/stocks/quote/AAPL
```

**Test Frontend:**
Open http://localhost:3000 in your browser

---

## 🔧 If Frontend Won't Start

1. **Check if port 3000 is in use:**
```bash
lsof -i :3000
```

2. **Kill any process using port 3000:**
```bash
lsof -ti:3000 | xargs kill -9
```

3. **Use a different port:**
Edit `frontend/vite.config.js` and change:
```javascript
server: {
  port: 3001,  // Change to any available port
  // ...
}
```

---

## 🎉 You're Ready!

Everything is set up. Just run both servers and start trading!

**Questions or issues?** Check the full documentation:
- `PROJECT_COMPLETE.md` - Complete overview
- `SETUP_GUIDE.md` - Detailed setup
- `frontend/README.md` - Frontend docs

