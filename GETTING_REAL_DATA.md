# Getting Real Flight Data from Frontier

## The Challenge

Frontier Airlines has **strong bot detection** (Cloudflare + PerimeterX/HUMAN) that blocks:
- ❌ Simple HTTP requests
- ❌ Cloudscraper
- ❌ Basic Playwright/Selenium without cookies

## ✅ Working Solution: Use Browser Cookies

Based on successful projects like [GWsearch](https://github.com/fly-metothemoon/GWsearch), the key is to **use cookies from your logged-in browser session**.

### Why This Works

When you're logged into Frontier in your browser:
1. Your browser has authentication cookies
2. Frontier's bot detection recognizes you as a legitimate user
3. By copying those cookies to the scraper, it appears as your logged-in session

## Step-by-Step Setup (Local Machine Only)

### Method 1: Export Cookies from Browser (Recommended)

#### Step 1: Install Browser Extension

Install a cookie export extension:

**Chrome/Edge:**
- [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
- [Cookie-Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)

**Firefox:**
- [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

#### Step 2: Login to Frontier

1. Open your browser
2. Go to https://www.flyfrontier.com
3. Login to your Frontier Miles account
4. Navigate to the flight search page

#### Step 3: Export Cookies

**Using Cookie-Editor:**
1. Click the extension icon
2. Click "Export" → "JSON"
3. Save as `backend/cookies.json`

**Using Get cookies.txt:**
1. Click the extension icon on flyfrontier.com
2. Choose "Export as JSON"
3. Save as `backend/cookies.json`

#### Step 4: Run the Scraper

```bash
cd backend
source venv/bin/activate
python scraper_with_cookies.py
```

The scraper will:
- ✅ Load your cookies
- ✅ Appear as your logged-in session
- ✅ Bypass bot detection
- ✅ Extract flight data

### Method 2: Let Playwright Use Your Browser

#### Option A: Use Persistent Browser Context

```python
# This uses your actual Chrome profile with saved cookies
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir="/path/to/your/chrome/profile",
        headless=False
    )
    page = browser.new_page()
    # You'll already be logged in!
```

**Chrome profile locations:**
- **Windows:** `C:\\Users\\YourName\\AppData\\Local\\Google\\Chrome\\User Data`
- **Mac:** `~/Library/Application Support/Google/Chrome`
- **Linux:** `~/.config/google-chrome`

#### Option B: Manual Cookie Collection

1. Run scraper with `headless=False`
2. Manually login in the browser window that opens
3. Scraper will auto-save cookies
4. Next time it will use saved cookies

## Understanding the HTML Structure

Once you can access the page, you need to **parse the HTML**.

### Finding the Right Selectors

1. **Open Flight Search Page**
   - Go to flyfrontier.com
   - Search for a flight
   - Wait for results to load

2. **Inspect the HTML** (F12 Developer Tools)
   - Right-click on a flight → "Inspect"
   - Look for patterns in the HTML

3. **Common Patterns**

Frontier likely uses patterns like:

```html
<!-- Flight Card -->
<div class="flight-card" data-flight-number="F9-1234">
  <!-- Departure Time -->
  <div class="departure">
    <time>08:30</time>
  </div>

  <!-- Arrival Time -->
  <div class="arrival">
    <time>10:15</time>
  </div>

  <!-- Pricing -->
  <div class="pricing">
    <div class="gowild-price">$0.99</div>
    <div class="regular-price">$89.99</div>
  </div>

  <!-- Flight Details -->
  <div class="details">
    <span class="duration">1h 45m</span>
    <span class="stops">Nonstop</span>
  </div>
</div>
```

Or they might embed data in JSON:

```html
<script type="application/json" id="flight-data">
{
  "flights": [
    {
      "flightNumber": "F9-1234",
      "departure": "08:30",
      "goWildPrice": 0.99
    }
  ]
}
</script>
```

### Updating the Parser

Edit `scraper_with_cookies.py` in the `parse_flights()` method:

```python
async def parse_flights(self, html_content: str, origin: str, destination: str, date: str):
    soup = BeautifulSoup(html_content, 'html.parser')
    flights = []

    # METHOD 1: Find JSON data (preferred if available)
    script_data = soup.find('script', type='application/json')
    if script_data:
        data = json.loads(script_data.string)
        # Parse the JSON structure

    # METHOD 2: Parse HTML elements
    flight_cards = soup.find_all('div', class_='flight-card')
    for card in flight_cards:
        flight = {
            'flight_number': card.get('data-flight-number'),
            'departure_time': card.find('div', class_='departure').find('time').text,
            'arrival_time': card.find('div', class_='arrival').find('time').text,
            'gowild_price': float(card.find('div', class_='gowild-price').text.replace('$', '')),
            # ... etc
        }
        flights.append(flight)

    return flights
```

## Integration with Main Application

Once scraping works, integrate it with the main app:

### Update `backend/scraper.py`

Replace the `FrontierScraper` class with the cookie-based version from `scraper_with_cookies.py`.

### Update `backend/main.py`

Make sure the API endpoints use the new scraper:

```python
from scraper_with_cookies import CookieBasedScraper

async def scrape_flights_background(origin: str, destination: str, date: str, db: Session):
    scraper = CookieBasedScraper()
    try:
        await scraper.start()
        flights = await scraper.search_flights(origin, destination, date)

        # Save to database
        for flight_data in flights:
            flight = Flight(**flight_data)
            db.add(flight)
        db.commit()
    finally:
        await scraper.close()
```

## Testing the Setup

### Test 1: Verify Cookies Work

```bash
python scraper_with_cookies.py
```

Expected output:
```
✅ Loaded 24 cookies
🔍 Navigating to flight search...
✅ Saved page to frontier_page.html
📊 Found 5 flights
```

### Test 2: Check Saved HTML

```bash
open frontier_page.html  # or just view in browser
```

Look for:
- Flight information displayed
- No "Access Denied" messages
- No CAPTCHA challenges

### Test 3: Full Integration

```bash
# Start backend
python main.py

# In another terminal, test API
curl -X POST "http://localhost:8000/api/scrape/search?origin=DEN&destination=LAX&date=2025-11-07"

# Wait 30 seconds, then check results
curl "http://localhost:8000/api/flights?origin=DEN&destination=LAX"
```

## Troubleshooting

### "Still getting 403"

- ✅ Make sure cookies are fresh (re-export them)
- ✅ Try logging in again on Frontier's website
- ✅ Export cookies while on flyfrontier.com domain
- ✅ Check cookies.json has valid data

### "No flights found"

- ✅ Check `frontier_page.html` - did the page load?
- ✅ Update selectors in `parse_flights()`
- ✅ Look for JSON data in script tags
- ✅ Use browser DevTools to find correct elements

### "Cookies expire quickly"

- ✅ Automate cookie refresh (login programmatically)
- ✅ Use persistent browser context (Method 2)
- ✅ Run scraper in non-headless mode and stay "logged in"

## Alternative Approaches

### If Cookies Don't Work

1. **Use Official Frontier Developer API**
   - Check https://developer.flyfrontier.com/
   - May require partnership/approval

2. **Use Third-Party Flight APIs**
   - Duffel API (has Frontier)
   - Aviation Edge
   - AirLabs

3. **Manual Data Entry**
   - Run the app with test data
   - Manually check Frontier and input GoWild flights
   - Less automated but guaranteed to work

## Why This Environment Can't Do It

The sandboxed environment where I'm running has:
- ❌ No ability to install Playwright browsers (403 errors)
- ❌ No access to bypass network restrictions
- ❌ No real browser with cookies
- ❌ Strong outbound filtering

**On your local machine, you'll have:**
- ✅ Full Playwright browser installation
- ✅ Your real browser cookies
- ✅ Direct internet access
- ✅ Ability to login and authenticate

## Next Steps

1. **Clone the repository to your local machine**
2. **Run the setup script** (`./setup.sh`)
3. **Export cookies from your browser**
4. **Test the scraper** with cookies
5. **Inspect the HTML** to find correct selectors
6. **Update the parser** in `scraper_with_cookies.py`
7. **Integrate** with the main app
8. **Deploy** and enjoy!

## Legal & Ethical Notes

⚠️ **Important:**
- Only use for personal flight searching
- Respect Frontier's Terms of Service
- Don't overload their servers (use rate limiting)
- Consider using official APIs when available
- This is for educational purposes

## Success Criteria

You'll know it's working when:

✅ Scraper loads with cookies
✅ No 403 errors
✅ HTML file contains flight data
✅ Parser extracts flight information
✅ Database gets populated
✅ Frontend displays real flights
✅ GoWild prices show correctly

Good luck! 🚀
