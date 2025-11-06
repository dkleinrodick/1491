# 🛫 Frontier GoWild Flight Scraper - START HERE

Welcome! This application helps you find Frontier Airlines GoWild pass flights.

---

## 🚀 I'm New to This - What Do I Read?

### If you're on **Windows** and know nothing about coding:
👉 **Read: `QUICK_START.md`** (20 minutes to get running)

Or for more detailed instructions:
👉 **Read: `WINDOWS_SETUP_GUIDE.md`** (complete walkthrough with troubleshooting)

### If you're on **Mac** or **Linux**:
👉 **Read: `SCRAPFLY_SETUP.md`** (technical setup guide)

---

## ⚡ Super Quick Overview

**What this does:**
- Scrapes Frontier Airlines GoWild flight availability
- Stores flight data in a database
- Provides a website to search and view flights

**What you need:**
- Python 3.11+
- Node.js 20+
- Scrapfly API key (free tier available)

**What you'll get:**
- A website running on your computer at http://localhost:5173
- Real-time flight scraping
- 882 Frontier routes to choose from

---

## 📋 What's in This Project?

```
Backend (Python FastAPI):
- Scrapes flights using Scrapfly.io
- Stores data in SQLite database
- 882 Frontier routes loaded
- REST API for frontend

Frontend (React + Vite):
- Search flights by route
- Filter GoWild-only flights
- Trigger scraping for specific routes
- Clean, modern interface
```

---

## 🎯 Choose Your Guide

### For Absolute Beginners (Windows)
**File**: `QUICK_START.md`
- Step-by-step Windows setup
- No prior knowledge needed
- ~20 minutes start to finish

### For Windows Users Who Want Details
**File**: `WINDOWS_SETUP_GUIDE.md`
- Complete walkthrough
- Troubleshooting section
- Explanations of what each step does

### For Activating Scrapfly API
**File**: `HOW_TO_ACTIVATE_SCRAPFLY.md`
- How to sign up for Scrapfly
- How to get your API key
- How to verify it works

### For Technical Users
**File**: `SCRAPFLY_SETUP.md`
- Technical implementation details
- API documentation
- Development setup

---

## ✅ Quick Status Check

Everything is ready to go! Here's what's complete:

- ✅ Backend (Python/FastAPI) - Complete
- ✅ Frontend (React/Vite) - Complete
- ✅ Scrapfly integration - Complete
- ✅ Database with 882 routes - Loaded
- ✅ Test data - 6 sample flights
- ✅ CSS selectors for parsing - Implemented
- ✅ GoWild URL (ftype=GW) - Implemented
- ⚠️ **Scrapfly API key - Needs activation**

---

## 🔑 Important: API Key Required

This app uses **Scrapfly.io** to bypass Frontier's bot detection.

**Current API Key**: `scp-live-c07f17fbff654e8188cd5308fa92018d`

**Status**: Needs activation

**What to do:**
1. Read: `HOW_TO_ACTIVATE_SCRAPFLY.md`
2. Sign up at https://scrapfly.io/ (free tier available)
3. Get your API key
4. Update `backend/.env` file if different

---

## 🎓 How It Works

1. **You choose a route** (e.g., ORD → CUN)
2. **The scraper runs** using Scrapfly to bypass bot detection
3. **Frontier's page loads** with JavaScript rendering
4. **Flight data is parsed** using CSS selectors
5. **Data is saved** to SQLite database
6. **You view flights** on the website

---

## 📁 File Guide

| File | What It Does |
|------|--------------|
| `QUICK_START.md` | Windows setup for beginners |
| `WINDOWS_SETUP_GUIDE.md` | Detailed Windows guide |
| `HOW_TO_ACTIVATE_SCRAPFLY.md` | API key activation guide |
| `SCRAPFLY_SETUP.md` | Technical documentation |
| `backend/scrapfly_scraper.py` | Main flight scraper |
| `backend/main.py` | FastAPI server |
| `backend/.env` | Configuration (API key here) |
| `frontend/src/App.jsx` | Website interface |

---

## 🐛 Common Issues

**403 Forbidden when scraping:**
→ Scrapfly API key not activated. Read `HOW_TO_ACTIVATE_SCRAPFLY.md`

**"python is not recognized":**
→ Python not installed or not in PATH. Reinstall Python.

**"npm is not recognized":**
→ Node.js not installed. Install from https://nodejs.org/

**No flights showing:**
→ Database is empty. Scrape some routes first using the API.

**Port already in use:**
→ Restart your computer and try again.

---

## 🎯 Test Case

To verify everything works, try scraping:

**Route**: ORD → CUN
**Date**: 2025-11-08

**Expected**: 2 flights
- 7:25 AM → 12:18 PM (Nonstop, ~$80)
- 10:35 AM → 1:19 PM (1 Stop, ~$85)

---

## 🌟 Features

- ✅ **Single-route scraping** - Save API credits
- ✅ **1-hour caching** - Don't re-scrape same route
- ✅ **882 Frontier routes** - All loaded in database
- ✅ **GoWild-specific** - Uses ftype=GW parameter
- ✅ **JavaScript rendering** - Handles dynamic content
- ✅ **Background processing** - Non-blocking scraping
- ✅ **REST API** - Full API documentation
- ✅ **Modern UI** - React with TailwindCSS

---

## 📞 Need Help?

1. **Read the guides** - Most questions are answered in:
   - `QUICK_START.md` (beginners)
   - `WINDOWS_SETUP_GUIDE.md` (detailed)
   - `HOW_TO_ACTIVATE_SCRAPFLY.md` (API key)

2. **Check error messages** - They often tell you what's wrong

3. **Common fixes:**
   - Restart everything
   - Make sure you're in the right folder
   - Check both backend AND frontend are running

---

## 🚀 Ready to Start?

### Windows Users (Beginners):
👉 Open `QUICK_START.md`

### Windows Users (Want Details):
👉 Open `WINDOWS_SETUP_GUIDE.md`

### Mac/Linux Users:
👉 Open `SCRAPFLY_SETUP.md`

### Just Need to Activate API:
👉 Open `HOW_TO_ACTIVATE_SCRAPFLY.md`

---

## 📊 What You'll See

**Backend Running:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Frontend Running:**
```
➜  Local:   http://localhost:5173/
```

**Website:**
- Clean interface
- Search flights by route
- Filter GoWild-only
- View flight details

**API Docs:**
- http://localhost:8000/docs
- Interactive API testing
- All endpoints documented

---

## 🎉 Success Looks Like This

1. Two command windows open (backend + frontend)
2. Website loads at http://localhost:5173
3. You see test flights on the page
4. You can search for flights
5. You can scrape new routes
6. Flights appear in your database
7. Everything works!

---

**Bottom Line**: Read `QUICK_START.md` if you're on Windows and new to this. It'll have you running in 20 minutes!

**Happy Flight Hunting!** ✈️
