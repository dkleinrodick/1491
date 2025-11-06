# Usage Guide

## Getting Started

After setting up the application (see [README.md](README.md)), follow these steps:

## 1. Start the Application

### Using Docker Compose
```bash
docker-compose up
```

### Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 2. Access the Application

Open your browser to: http://localhost:5173

## 3. Understanding the Interface

### Search Form

The main search form has several filters:

1. **Origin** - Select departure airport
2. **Destination** - Select arrival airport (populated based on origin)
3. **Date** - Choose "Today" or "Tomorrow"
4. **GoWild Only** - Toggle to show only GoWild available flights

### Action Buttons

#### Search Cached Flights
- Searches the database for existing flight data
- Fast, instant results
- Use this first to check if data already exists

#### Trigger New Search
- Starts a new scraping job for the specific route
- Requires both origin AND destination
- Takes 30-60 seconds
- Use when you need fresh data or data doesn't exist

#### Bulk Search (All Destinations)
- Scrapes all destinations from selected origin
- Takes several minutes (many routes)
- Best done once per day per origin
- Useful for exploring all options

## 4. Common Workflows

### Workflow 1: Quick Search for Specific Route

```
1. Select Origin: DEN (Denver)
2. Select Destination: LAX (Los Angeles)
3. Select Date: Tomorrow
4. Check "GoWild Only"
5. Click "Search Cached Flights"
```

If no results:
```
6. Click "Trigger New Search"
7. Wait 30-60 seconds
8. Click "Search Cached Flights" again
```

### Workflow 2: Explore All Options from Home Airport

```
1. Select Origin: DEN (Denver)
2. Leave Destination: "All Destinations"
3. Select Date: Today
4. Click "Bulk Search (All Destinations)"
5. Wait 5-10 minutes
6. Come back and search with filters
```

### Workflow 3: Find Cheapest GoWild Flights Today

```
1. Don't select any filters initially
2. Check "GoWild Only"
3. Click "Search Cached Flights"
4. Browse all available GoWild flights
5. Sort mentally by price in the cards
```

## 5. Understanding Flight Cards

Each flight card shows:

- **Origin → Destination** - Route information
- **Flight Number** - Frontier flight number
- **GoWild Badge** - Green badge if available with GoWild pass
- **Departure Info** - Date and time of departure
- **Arrival Info** - Date and time of arrival
- **Duration** - Total flight time
- **Stops** - Number of connections (0 = nonstop)
- **GoWild Price** - Price with GoWild pass (main price)
- **Regular Price** - Standard ticket price (crossed out)

## 6. Tips & Tricks

### Best Practices

1. **Run Bulk Search Daily**
   - Pick your home airport
   - Run bulk search once per day
   - Check results throughout the day

2. **Check Multiple Times**
   - Flight availability changes frequently
   - Morning availability may differ from evening
   - Check before booking on Frontier's site

3. **Use Filters Strategically**
   - Start broad, then narrow down
   - Check "GoWild Only" to focus on pass flights
   - Try different date combinations

4. **Plan Ahead**
   - Trigger searches for tomorrow evening
   - Check first thing in the morning
   - GoWild availability is dynamic

### Limitations

- **No Real-Time Booking**: This tool only shows availability, you must book on Frontier's website
- **Cache Times**: Data may be up to 1 hour old
- **Scraping Time**: New searches take 30-60 seconds per route
- **Rate Limits**: Don't trigger too many searches at once

## 7. Troubleshooting

### "No flights found"

**Solutions:**
- Trigger a new search for that specific route
- Try bulk search for the origin
- Check if route actually exists (some combinations don't fly)
- Verify Frontier operates that route

### Search is slow

**Reasons:**
- Scraper is bypassing bot detection (takes time)
- Multiple requests in queue
- Frontier's website is slow

**Solutions:**
- Be patient, wait 60 seconds
- Don't click multiple times
- Check backend logs for errors

### Frontend won't connect

**Check:**
1. Backend is running on port 8000
2. Frontend is running on port 5173
3. No firewall blocking connections
4. Check browser console for errors

### Backend errors

**Common issues:**
1. **Playwright not installed**: Run `playwright install chromium`
2. **Database missing**: Run `python -c "from database import init_db; init_db()"`
3. **Port already in use**: Change port in `.env`
4. **Missing dependencies**: Run `pip install -r requirements.txt`

## 8. Advanced Usage

### API Direct Access

You can use the API directly without the frontend:

#### Get All GoWild Flights
```bash
curl "http://localhost:8000/api/flights?gowild_only=true&limit=50"
```

#### Get Flights for Specific Route
```bash
curl "http://localhost:8000/api/flights?origin=DEN&destination=LAX&date=2025-11-07"
```

#### Trigger Search
```bash
curl -X POST "http://localhost:8000/api/scrape/search?origin=DEN&destination=LAX&date=2025-11-07"
```

#### Get Statistics
```bash
curl "http://localhost:8000/api/stats"
```

### Using with Scripts

You can integrate the API into your own scripts:

**Python Example:**
```python
import requests

# Search for flights
response = requests.get('http://localhost:8000/api/flights', params={
    'origin': 'DEN',
    'gowild_only': True,
    'limit': 10
})

flights = response.json()
for flight in flights:
    print(f"{flight['origin']} -> {flight['destination']}: ${flight['gowild_price']}")
```

**JavaScript Example:**
```javascript
// Fetch GoWild flights
fetch('http://localhost:8000/api/flights?gowild_only=true')
  .then(res => res.json())
  .then(flights => {
    flights.forEach(flight => {
      console.log(`${flight.origin} -> ${flight.destination}: $${flight.gowild_price}`);
    });
  });
```

### Scheduled Scraping

For production use, set up cron jobs or scheduled tasks:

**Linux/Mac cron (daily at 6 AM):**
```bash
0 6 * * * curl -X POST "http://localhost:8000/api/scrape/bulk?origin=DEN&days=2"
```

**Windows Task Scheduler:**
Create a task that runs:
```powershell
curl.exe -X POST "http://localhost:8000/api/scrape/bulk?origin=DEN&days=2"
```

## 9. Production Deployment

See deployment guides:
- [Backend Deployment](backend/README.md#production)
- [Frontend Deployment](frontend/README.md#deployment)

## 10. Getting Help

- Check the [README.md](README.md)
- Review [Backend Documentation](backend/README.md)
- Review [Frontend Documentation](frontend/README.md)
- Check application logs for errors
- Look at browser console (F12) for frontend issues

## Important Notes

⚠️ **This tool is for educational purposes only**

- Always verify availability on Frontier's official website before booking
- Respect Frontier Airlines' Terms of Service
- Don't abuse the scraping functionality
- Consider rate limits and be responsible
- This is not affiliated with Frontier Airlines

## Legal & Ethical Use

✅ **Acceptable Use:**
- Personal flight searching
- Checking availability for your own travel
- Educational purposes
- Learning web scraping techniques

❌ **Not Acceptable:**
- Commercial use without permission
- Reselling flight data
- Overwhelming Frontier's servers
- Bypassing official booking systems
- Any illegal activities
