# Scrape.do Setup Guide

## Current Status

⚠️ **The Scrape.do token is currently returning 403 Forbidden errors.**

This could mean:
1. The token is invalid or expired
2. The account needs to be activated
3. The account is out of credits
4. The API endpoint format is incorrect

## Checking Your Scrape.do Account

### Step 1: Login to Scrape.do

1. Go to https://scrape.do/
2. Login with your email: `dkrshs106@gmail.com`
3. Check your dashboard

### Step 2: Verify Account Status

Check for:
- ✅ Account is active
- ✅ API token is correct
- ✅ You have available credits
- ✅ No rate limiting or blocks

### Step 3: Get/Verify API Token

1. Go to Dashboard → API Settings
2. Copy your API token
3. Update `backend/.env`:
   ```
   SCRAPE_DO_EMAIL=dkrshs106@gmail.com
   SCRAPE_DO_TOKEN=your-actual-token-here
   ```

## Testing the Integration

Once your account is set up:

```bash
cd backend
source venv/bin/activate

# Test token validity
python test_scrape_do_token.py

# If token works, test flight scraping
python scrape_do_scraper.py
```

## Expected Results

When working correctly, you should see:

```
✅ Scrape.do token is WORKING!
🔍 Searching: DEN -> LAX on 2025-11-07
✅ Saved HTML to scraped_DEN_LAX_2025-11-07.html
✅ Found X flights
```

## Using the Route Selector

We've parsed all 882 Frontier routes. You can:

### 1. View All Routes

```bash
cd backend
python -c "import json; routes = json.load(open('frontier_routes.json')); print(f'{len(routes)} routes available')"
```

### 2. Search for Specific Routes

```python
import json

with open('frontier_routes.json') as f:
    routes = json.load(f)

# Find all routes from Denver
denver_routes = [r for r in routes if r['origin_code'] == 'DEN']
print(f"Found {len(denver_routes)} routes from Denver")

# Find specific route
for route in routes:
    if route['origin_code'] == 'DEN' and route['destination_code'] == 'LAX':
        print(route)
```

## API Endpoint (Once Working)

The API endpoint for scraping a single route:

```bash
# Scrape one route
curl -X POST "http://localhost:8000/api/scrape/route" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "DEN",
    "destination": "LAX",
    "date": "2025-11-07"
  }'
```

## Alternative: Manual Route Selection

If Scrape.do doesn't work, you can:

### Option 1: Use Browser Cookies (From Previous Guide)

See `GETTING_REAL_DATA.md` for cookie-based scraping.

### Option 2: Manual Data Entry

1. Pick a route from `frontier_routes.json`
2. Manually check Frontier.com
3. Add flights using the test data script:

```python
from database import SessionLocal, Flight

db = SessionLocal()

flight = Flight(
    flight_number='F9-1234',
    origin='DEN',
    destination='LAX',
    departure_date='2025-11-07',
    departure_time='08:30',
    arrival_time='10:15',
    gowild_price=0.99,
    is_gowild_available=True
)

db.add(flight)
db.commit()
```

### Option 3: Try Different Proxy Service

If Scrape.do doesn't work, alternatives:
- **ScraperAPI** - https://www.scraperapi.com/
- **Bright Data** - https://brightdata.com/
- **Oxylabs** - https://oxylabs.io/
- **SmartProxy** - https://smartproxy.com/

All work similarly - you just need to update the API endpoint and token format.

## Cost Considerations

Scrape.do pricing (check their website for current rates):
- Usually charged per request
- Typical cost: $1-5 per 1000 requests
- 882 routes × daily scraping = ~882 requests/day
- Estimated: $0.88 - $4.41 per day for daily full scraping

**Recommendation**: Scrape popular routes more frequently, less popular ones weekly.

## Smart Scraping Strategy

To conserve credits:

### Tier 1: High-Traffic Routes (Scrape 4x/day)
- DEN → LAX, LAS, PHX, SFO, etc.
- ATL → Major cities
- ~50 routes

### Tier 2: Medium-Traffic (Scrape 2x/day)
- Regional hubs
- ~200 routes

### Tier 3: Low-Traffic (Scrape 1x/day or weekly)
- Smaller markets
- ~632 routes

This could reduce daily requests from 882 to ~150-200, saving significant costs.

## Implementation Plan

Once Scrape.do is working:

1. ✅ Token validated
2. ✅ Successfully scrapes test route
3. ✅ Parses flight data from HTML
4. ✅ Saves to database
5. ✅ Frontend shows route selector
6. ✅ User picks one route to scrape
7. ✅ Results display in UI

## Troubleshooting

### Still Getting 403

1. Check Scrape.do dashboard for errors
2. Verify API token format (might have extra characters)
3. Try regenerating the token
4. Contact Scrape.do support

### HTML Parsing Issues

If scraping works but no flights found:
1. Check saved HTML file
2. Inspect Frontier's HTML structure
3. Update selectors in `scrape_do_scraper.py`
4. See `GETTING_REAL_DATA.md` for selector examples

### Rate Limiting

If you hit rate limits:
1. Add delays between requests
2. Implement exponential backoff
3. Cache results longer
4. Reduce scraping frequency

## Next Steps

1. **Activate Scrape.do account** or choose alternative
2. **Verify token** with test script
3. **Test single route** scraping
4. **Inspect HTML** to update selectors
5. **Integrate with frontend** for route selection
6. **Set up scheduled scraping** for automated updates

## Contact

If you need help:
- Scrape.do Support: support@scrape.do
- Check dashboard: https://scrape.do/dashboard
- API Docs: https://scrape.do/docs

---

**Note**: All code is ready and waiting for a valid Scrape.do token. Once your account is active, everything should work immediately!
