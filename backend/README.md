# Backend - Frontier GoWild Flight Finder

FastAPI backend with Playwright scraper for Frontier Airlines GoWild flights.

## Features

- **Anti-Detection Scraping**: Uses Playwright with stealth techniques
- **RESTful API**: FastAPI endpoints for flight data
- **Background Jobs**: Async scraping without blocking requests
- **SQLite Database**: Persistent flight data storage
- **Rate Limiting**: Prevents overwhelming Frontier's servers
- **CORS Enabled**: Works with frontend applications

## Setup

### Prerequisites

- Python 3.11 or higher
- pip or poetry

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

4. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize database:
```bash
python -c "from database import init_db; init_db()"
```

## Running

### Development Server

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- http://localhost:8000
- API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Get Flights
```
GET /api/flights?origin=DEN&destination=LAX&date=2025-11-07&gowild_only=true
```

Query Parameters:
- `origin`: Origin airport code (optional)
- `destination`: Destination airport code (optional)
- `date`: Departure date YYYY-MM-DD (optional)
- `gowild_only`: Show only GoWild available flights (default: false)
- `limit`: Max results (default: 100)

### Get Origins
```
GET /api/origins
```

Returns list of all available origin airports.

### Get Destinations
```
GET /api/destinations?origin=DEN
```

Returns list of all available destinations (optionally filtered by origin).

### Trigger Flight Search
```
POST /api/scrape/search?origin=DEN&destination=LAX&date=2025-11-07
```

Triggers a background scrape for specific route and date.

### Trigger Bulk Scrape
```
POST /api/scrape/bulk?origin=DEN&days=2
```

Triggers bulk scrape for all destinations from origin for N days.

### Get Statistics
```
GET /api/stats
```

Returns database statistics.

## Testing the Scraper

Test the scraper directly:

```bash
python scraper.py
```

This will run a test search and show results.

## Anti-Detection Features

The scraper implements multiple anti-detection techniques:

1. **Browser Fingerprint Masking**
   - Removes `navigator.webdriver` flag
   - Fakes plugins and languages
   - Adds chrome runtime object

2. **Human-Like Behavior**
   - Random delays between actions
   - Mouse movement simulation
   - Realistic viewport and user agent

3. **Stealth Arguments**
   - Disables automation-controlled flags
   - Proper window sizing
   - Standard browser headers

4. **Rate Limiting**
   - Delays between requests
   - Respects Frontier's servers

## Configuration

Edit `.env` file to customize:

```env
# Run in headless mode (no browser window)
SCRAPER_HEADLESS=true

# Request timeout in milliseconds
SCRAPER_TIMEOUT=30000

# Maximum retry attempts
SCRAPER_MAX_RETRIES=3
```

## Troubleshooting

### Playwright Installation Issues

If `playwright install` fails:
```bash
playwright install-deps chromium
playwright install chromium
```

### Bot Detection

If you're getting blocked:
1. Set `SCRAPER_HEADLESS=false` to see what's happening
2. Increase delays in `scraper.py`
3. Check error screenshots saved to the backend directory
4. Consider using residential proxies (not implemented yet)

### Database Issues

Reset the database:
```bash
rm gowild.db
python -c "from database import init_db; init_db()"
```

## TODO / Future Enhancements

- [ ] Implement actual HTML parsing based on Frontier's structure
- [ ] Add proxy rotation support
- [ ] Implement Redis caching
- [ ] Add authentication/API keys
- [ ] Scheduled scraping with APScheduler
- [ ] Better error handling and retry logic
- [ ] Parse GoWild-specific pricing indicators
- [ ] Add support for browser cookie import (like the GitHub project)
- [ ] Implement CAPTCHA solving (if needed)

## Important Notes

⚠️ **Disclaimer**: This tool is for educational purposes. Always:
- Respect Frontier Airlines' Terms of Service
- Implement rate limiting
- Don't overload their servers
- Consider using official APIs when available

## Architecture

```
┌─────────────────┐
│   FastAPI App   │
│   (main.py)     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼─────────┐
│ DB    │ │  Scraper   │
│Model  │ │ (Playwright)│
└───────┘ └────────────┘
```

## Development

### Adding New Endpoints

1. Add route to `main.py`
2. Update this README
3. Test with `/docs` interface

### Updating Scraper

1. Inspect Frontier's website HTML
2. Update selectors in `scraper.py` `parse_flights()` method
3. Test with `python scraper.py`

### Database Migrations

For schema changes:
```bash
# Create new SQLAlchemy models in database.py
# Then recreate database
rm gowild.db
python -c "from database import init_db; init_db()"
```

For production, consider using Alembic for migrations.
