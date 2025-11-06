# Frontier GoWild Flight Finder

A web application to search and display available Frontier Airlines GoWild pass flights.

## Features

- 🔍 Search all available GoWild flights from any origin
- 📅 View flights for today and tomorrow
- 💰 Display GoWild pass pricing
- 🚀 Fast, cached results
- 🎨 Clean, modern UI

## Tech Stack

### Backend
- Python 3.11+
- FastAPI - Modern API framework
- Playwright with playwright-stealth - Anti-detection web scraping
- SQLite - Flight data storage
- Pydantic - Data validation

### Frontend
- React with Vite
- TailwindCSS - Styling
- Axios - API calls

## Architecture

```
┌─────────────┐
│   Frontend  │
│   (React)   │
└──────┬──────┘
       │
       │ HTTP API
       │
┌──────▼──────┐     ┌──────────────┐
│   FastAPI   │────►│   SQLite DB  │
│   Backend   │     │              │
└──────┬──────┘     └──────────────┘
       │
       │ Scheduled Jobs
       │
┌──────▼──────────────────┐
│  Playwright Scraper     │
│  (Anti-Bot Detection)   │
└─────────────────────────┘
```

## How It Works

1. **Scraper**: Uses Playwright with stealth plugins to bypass Frontier's bot detection
2. **API**: FastAPI serves cached flight data and triggers scraper updates
3. **Database**: Stores flight availability with timestamps
4. **Frontend**: React app displays flights with filtering options

## Anti-Bot Strategy

- Playwright-stealth to mask automation
- Randomized delays between requests
- Browser fingerprint randomization
- Cookie persistence from authenticated sessions
- Rate limiting to avoid detection

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd 1491

# Start everything with Docker
docker-compose up
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

### Option 2: Automated Setup Script

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

### Option 3: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Create environment file
cp .env.example .env

# Initialize database
python -c "from database import init_db; init_db()"

# Run the backend
python main.py
```

Backend will be available at http://localhost:8000

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
# or
bun install

# Create environment file
cp .env.example .env

# Run the frontend
npm run dev
# or
bun run dev
```

Frontend will be available at http://localhost:5173

## Detailed Documentation

See `/backend/README.md` and `/frontend/README.md` for detailed setup instructions.

## Disclaimer

This project is for educational purposes. Users are responsible for complying with Frontier Airlines' Terms of Service. Use responsibly and consider rate limits.

## Inspiration

Inspired by:
- https://www.the1491club.com/
- https://searchgwp.com/
- https://gowilder.net/
- https://github.com/fly-metothemoon/GWsearch
