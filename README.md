# 🛫 Frontier GoWild Flight Scraper

Find the best Frontier Airlines GoWild pass flight deals automatically!

![Status](https://img.shields.io/badge/status-ready-brightgreen)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20mac%20%7C%20linux-blue)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Node](https://img.shields.io/badge/node-20+-green)

---

## ⚡ Quick Start (Windows Users - Complete Beginners)

**Never coded before? Start here!**

1. **Install Python** from https://python.org (check "Add to PATH")
2. **Install Node.js** from https://nodejs.org
3. **Download this project** (green "Code" button → Download ZIP)
4. **Follow the guide**: Open **[QUICK_START.md](QUICK_START.md)**

**You'll be running in ~20 minutes!**

---

## 📖 Choose Your Guide

| I am... | Read this file... |
|---------|------------------|
| 👶 New to coding (Windows) | **[QUICK_START.md](QUICK_START.md)** |
| 💻 Windows user who wants details | **[WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md)** |
| 🔑 Need to activate Scrapfly API | **[HOW_TO_ACTIVATE_SCRAPFLY.md](HOW_TO_ACTIVATE_SCRAPFLY.md)** |
| 🧑‍💻 Technical user / Mac / Linux | **[SCRAPFLY_SETUP.md](SCRAPFLY_SETUP.md)** |
| ❓ Not sure where to start | **[START_HERE.md](START_HERE.md)** |

---

## ✨ Features

- ✅ **Single-route scraping** - Save API credits by choosing specific routes
- ✅ **GoWild-specific** - Direct access to GoWild flights via `ftype=GW`
- ✅ **1-hour caching** - Avoid re-scraping same route
- ✅ **882 routes loaded** - All Frontier routes in database
- ✅ **Modern UI** - React + Vite + TailwindCSS
- ✅ **REST API** - Full API documentation at `/docs`
- ✅ **Background processing** - Non-blocking scraping

---

## 🎯 What This Does

- **Scrapes** Frontier Airlines GoWild flight availability
- **Stores** flight data in a local database
- **Provides** a clean web interface to search flights
- **Supports** all 882 Frontier routes
- **Bypasses** bot detection using Scrapfly.io

---

## 📊 Tech Stack

### Backend
- Python 3.11+
- FastAPI - Modern API framework
- Scrapfly SDK - Anti-detection web scraping
- BeautifulSoup4 - HTML parsing
- SQLite - Flight data storage
- SQLAlchemy - Database ORM
- Pydantic - Data validation

### Frontend
- React 18 with Vite
- TailwindCSS - Styling
- Axios - API calls

## 🏗️ Architecture

```
┌─────────────┐
│   Frontend  │  ← React + Vite + TailwindCSS
│  (Browser)  │    http://localhost:5173
└──────┬──────┘
       │
       │ HTTP API
       │
┌──────▼──────┐     ┌──────────────┐
│   FastAPI   │────►│  SQLite DB   │ ← 882 routes + flight data
│   Backend   │     │              │
└──────┬──────┘     └──────────────┘
       │
       │ Background Jobs
       │
┌──────▼──────────────────┐
│  Scrapfly.io           │ ← JavaScript rendering + bot bypass
│  (Cloud Service)       │
└──────┬─────────────────┘
       │
       │ Fetches
       │
┌──────▼──────────────────┐
│  Frontier Booking Page  │ ← GoWild flights (ftype=GW)
│  (booking.flyfrontier)  │
└─────────────────────────┘
```

## 🎓 How It Works

1. **You choose** a route (e.g., ORD → CUN) and date
2. **Backend** builds GoWild URL with `ftype=GW` parameter
3. **Scrapfly** loads the page with JavaScript rendering
4. **Scraper** parses HTML using CSS selectors
5. **Database** stores flight times, prices, duration, stops
6. **Frontend** displays flights with search/filter options

## 🛡️ Anti-Bot Strategy

- **Scrapfly.io** - Professional proxy service with bot bypass
- **JavaScript Rendering** - `render_js=True` handles dynamic content
- **Wait for Selector** - Ensures flights are loaded before parsing
- **1-Hour Caching** - Prevents excessive requests
- **Single-Route Scraping** - User controls what gets scraped

## 🚀 Quick Setup

### For Complete Beginners (Windows)

**Read:** [QUICK_START.md](QUICK_START.md) - 20-minute setup guide

### For Everyone Else

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python main.py
```

**Frontend (new terminal):**
```bash
cd frontend
npm install
npm run dev
```

**Browser:**
Open http://localhost:5173

**API Key Required:**
See [HOW_TO_ACTIVATE_SCRAPFLY.md](HOW_TO_ACTIVATE_SCRAPFLY.md)

---

## 🔑 Scrapfly API Key

This app uses **Scrapfly.io** to bypass bot detection.

1. Sign up at https://scrapfly.io/ (1,000 free requests)
2. Copy your API key
3. Update `backend/.env`:
   ```
   SCRAPFLY_API_KEY=your-api-key-here
   ```

**Detailed guide:** [HOW_TO_ACTIVATE_SCRAPFLY.md](HOW_TO_ACTIVATE_SCRAPFLY.md)

---

## 🧪 Test It Works

Scrape the test route:

**Via Browser:**
1. Go to http://localhost:8000/docs
2. Find **POST /api/scrape/single-route**
3. Try it out with: `origin=ORD`, `destination=CUN`, `date=2025-11-08`
4. Check http://localhost:5173 for results

**Via Command Line:**
```bash
curl -X POST "http://localhost:8000/api/scrape/single-route?origin=ORD&destination=CUN&date=2025-11-08"
```

**Expected:** 2 flights (7:25 AM and 10:35 AM departures)

---

## 📚 Complete Documentation

**All guides are in the root directory:**
- [QUICK_START.md](QUICK_START.md) - Beginner Windows setup
- [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md) - Detailed Windows guide
- [HOW_TO_ACTIVATE_SCRAPFLY.md](HOW_TO_ACTIVATE_SCRAPFLY.md) - API key activation
- [SCRAPFLY_SETUP.md](SCRAPFLY_SETUP.md) - Technical documentation
- [START_HERE.md](START_HERE.md) - Guide selector

---

## 🛠️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/flights` | GET | Get all flights from database |
| `/api/routes` | GET | Get all 882 Frontier routes |
| `/api/scrape/single-route` | POST | Scrape a specific route |
| `/api/stats` | GET | Database statistics |
| `/docs` | GET | Interactive API documentation |

**Example Usage:**
```bash
# Get GoWild flights from ORD to CUN
curl "http://localhost:8000/api/flights?origin=ORD&destination=CUN&gowild_only=true"

# Scrape a new route
curl -X POST "http://localhost:8000/api/scrape/single-route?origin=DEN&destination=LAX&date=2025-11-10"

# Get all routes from Chicago
curl "http://localhost:8000/api/routes?origin=ORD"
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| 403 Forbidden when scraping | Scrapfly API key not activated. See [HOW_TO_ACTIVATE_SCRAPFLY.md](HOW_TO_ACTIVATE_SCRAPFLY.md) |
| "python is not recognized" | Python not in PATH. Reinstall and check "Add Python to PATH" |
| "npm is not recognized" | Node.js not installed. Get it from https://nodejs.org/ |
| No flights showing | Database is empty. Scrape routes first |
| Port already in use | Something else using port 8000/5173. Restart computer or change ports |

**More help:** See [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md#troubleshooting)

---

## 📂 Project Structure

```
.
├── backend/
│   ├── main.py                  # FastAPI server
│   ├── scrapfly_scraper.py      # Flight scraper
│   ├── database.py              # Database models (Flight, Route)
│   ├── config.py                # Configuration
│   ├── .env                     # API key (you edit this!)
│   ├── requirements.txt         # Python dependencies
│   └── gowild.db               # SQLite database (auto-created)
│
├── frontend/
│   ├── src/App.jsx             # React app
│   ├── package.json            # Node dependencies
│   └── vite.config.js          # Vite config
│
└── Documentation/
    ├── QUICK_START.md          # Beginner Windows guide ← START HERE
    ├── WINDOWS_SETUP_GUIDE.md  # Detailed Windows guide
    ├── HOW_TO_ACTIVATE_SCRAPFLY.md  # API key guide
    ├── SCRAPFLY_SETUP.md       # Technical documentation
    └── START_HERE.md           # Guide selector
```

---

## 💡 Key Features Explained

### GoWild-Specific URL
The scraper uses `ftype=GW` parameter to request **only GoWild flights**:
```
https://booking.flyfrontier.com/Flight/InternalSelect?o1=ORD&d1=CUN&dd1=2025-11-08&adt=1&ftype=GW
```
No need to click checkboxes or filter mixed results!

### Cost Management
- **Single-route scraping** - Choose which routes to scrape
- **1-hour caching** - Won't re-scrape same route within 1 hour
- **Free tier friendly** - Works great with Scrapfly's 1,000 free requests

### Database
- **882 Frontier routes** preloaded
- **6 test flights** included for demo
- **SQLite** - No setup required, just a file

---

## 🎯 What You'll See

**When Backend Starts:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**When Frontend Starts:**
```
  ➜  Local:   http://localhost:5173/
```

**Website Features:**
- Search by origin/destination
- Filter GoWild-only flights
- View times, prices, duration, stops
- Trigger scraping for specific routes

**API Documentation:**
- Interactive testing at http://localhost:8000/docs
- Try endpoints right in the browser
- See request/response examples

---

## ⚠️ Disclaimer

This project is for **personal use and educational purposes only**. Users are responsible for complying with Frontier Airlines' Terms of Service. Use responsibly and don't overwhelm their servers with requests.

---

## 💼 Inspiration

Inspired by:
- https://www.the1491club.com/
- https://searchgwp.com/
- https://gowilder.net/
- https://github.com/fly-metothemoon/GWsearch

---

## 📜 License

MIT License - Use freely!

---

## 🎉 Ready to Start?

👉 **Windows Beginners:** Open [QUICK_START.md](QUICK_START.md)

👉 **Want Details:** Open [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md)

👉 **Mac/Linux:** Open [SCRAPFLY_SETUP.md](SCRAPFLY_SETUP.md)

---

**Happy flight hunting!** ✈️
