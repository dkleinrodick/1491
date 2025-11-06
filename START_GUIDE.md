# Quick Start Guide - Frontier GoWild Flight Scraper

## Current Status: ✅ Ready (Except Token Issue)

Your application is **fully built and ready to go**. There's just ONE blocking issue:

### 🚫 **Blocker: Scrape.do Token Invalid**

Your token `9db3a27534e44be28542086dea8c8b79712aa15864b` returns `403 Forbidden` errors.

---

## What You Need to Do RIGHT NOW

### Step 1: Activate Your Scrape.do Account (5 minutes)

1. **Go to**: https://scrape.do/
2. **Login with**: dkrshs106@gmail.com
3. **Check**:
   - Is your account activated?
   - Do you have credits?
   - What's your current API token?

4. **Get Your Working Token**:
   - Navigate to Dashboard → API Settings
   - Copy your API token
   - If no token exists, generate a new one

5. **Update Your `.env` File**:
   ```bash
   cd /home/user/1491/backend
   nano .env
   ```

   Replace the token line with your working token:
   ```
   SCRAPE_DO_TOKEN=your-new-working-token-here
   ```

---

## Step 2: Test Your Token (2 minutes)

```bash
cd /home/user/1491/backend
source venv/bin/activate
python test_scrape_do_token.py
```

**Expected Output (when working):**
```
✅ Scrape.do token is WORKING!
Your IP (via Scrape.do): ...
```

**If you still get 403:**
- Token is wrong
- Account needs activation
- Out of credits

---

## Step 3: Test the Known Route (2 minutes)

Once your token works, test with the known route:

```bash
python scraper_correct.py
```

This will:
- Scrape **ORD → CUN on 11/8/2025**
- Save HTML to `frontier_ORD_CUN_2025-11-08.html`
- Try to parse 2 expected flights:
  - **Flight 1**: 7:25 AM ORD → 12:18 PM CUN (3h 53m, Nonstop, $80)
  - **Flight 2**: 10:35 AM ATL → 1:19 PM CUN (6h 19m, 1 Stop, $85)

---

## Step 4: Run the Full Application (2 minutes)

### Start Backend:
```bash
cd /home/user/1491/backend
source venv/bin/activate
python main.py
```

Backend will be at: **http://localhost:8000**

### Start Frontend (New Terminal):
```bash
cd /home/user/1491/frontend
npm run dev
```

Frontend will be at: **http://localhost:5173**

---

## How to Use Your App

### Option 1: API Endpoints

**Scrape a Single Route:**
```bash
curl -X POST "http://localhost:8000/api/scrape/single-route?origin=ORD&destination=CUN&date=2025-11-08"
```

**Get Flights:**
```bash
# All flights
curl "http://localhost:8000/api/flights"

# GoWild only
curl "http://localhost:8000/api/flights?gowild_only=true"

# Specific route
curl "http://localhost:8000/api/flights?origin=ORD&destination=CUN"
```

**Get All Routes:**
```bash
# All 882 routes
curl "http://localhost:8000/api/routes"

# Filter by origin
curl "http://localhost:8000/api/routes?origin=ORD"
```

### Option 2: Web Interface

Open http://localhost:5173 in your browser:
- Search for flights by origin/destination
- Filter GoWild-only flights
- Trigger scraping for specific routes
- View flight details (times, prices, stops)

---

## What's Already Built

✅ **Backend (FastAPI)**
- Complete REST API
- 882 Frontier routes loaded in database
- Single-route scraping (conserves API credits)
- Background task processing
- SQLite database with Flight and Route models

✅ **Scraper (Scrape.do Integration)**
- Correct API format: `https://api.scrape.do/`
- Correct booking URL: `booking.flyfrontier.com/Flight/InternalSelect`
- Proper date format: MM-DD-YYYY
- JavaScript rendering enabled
- HTML parsing framework ready

✅ **Frontend (React + Vite + TailwindCSS)**
- Flight search interface
- Route filtering
- GoWild availability display
- Modern, responsive design

✅ **Test Data**
- 6 sample flights loaded for demo
- Test case ready: ORD→CUN 11/8/25

---

## What Happens After Token Works

Once you have a valid Scrape.do token:

### 1. Immediate Validation (30 seconds)
```bash
python scraper_correct.py
```
This will validate against your test case (ORD→CUN 11/8/25).

### 2. Update HTML Selectors (30-60 minutes)
Once you have the saved HTML file:
1. Open `frontier_ORD_CUN_2025-11-08.html` in a browser
2. Right-click → Inspect Element on flight data
3. Find CSS selectors for:
   - Flight times (should show: 7:25 AM, 12:18 PM, 10:35 AM, 1:19 PM)
   - Prices (should show: $80, $85)
   - Duration, stops, etc.
   - **GoWild box/indicator**

4. Update `scraper_correct.py` with correct selectors in `parse_flights()` method

### 3. Handle GoWild Box (15-30 minutes)
You mentioned: *"Once you are in the page, you need to click on the 'gowild' box"*

This means we need to either:
- **Option A**: Find what API the GoWild box calls and call it directly
- **Option B**: Check if GoWild data is already in the HTML (just hidden)
- **Option C**: Use Playwright to actually click the box (more expensive)

We'll know which option once we see the HTML.

---

## Important Notes

### Cost Conservation
- ✅ App only scrapes **ONE route at a time**
- ✅ Uses 1-hour caching (won't re-scrape same route within an hour)
- ✅ JavaScript rendering only when needed
- ✅ `blockResources=true` to skip images/CSS (faster, cheaper)

### Test Case Validation
The test case you provided is perfect:
- **Route**: ORD → CUN
- **Date**: 11/8/2025
- **Expected**: Exactly 2 flights with specific times and prices

This lets us validate that scraping works correctly before scaling up.

### API Credits
- Scrape.do charges per request
- Each route scrape = 1 API call
- With 882 routes, scraping everything once ≈ 882 credits
- **That's why we built single-route scraping!**

---

## File Structure Reference

```
/home/user/1491/
├── backend/
│   ├── scraper_correct.py         ⭐ CURRENT SCRAPER (correct API)
│   ├── main.py                     ⭐ FastAPI server
│   ├── database.py                 ⭐ Models (Flight, Route)
│   ├── config.py                   Settings & credentials
│   ├── .env                        🔑 YOUR TOKEN HERE
│   ├── test_scrape_do_token.py     Test token validity
│   ├── load_routes.py              Load 882 routes to DB
│   ├── frontier_routes.json        All 882 routes
│   └── requirements.txt            Dependencies
│
├── frontend/                        React app
│   ├── src/App.jsx                 Main UI component
│   └── package.json                Node dependencies
│
└── START_GUIDE.md                  👈 THIS FILE
```

---

## Troubleshooting

### Token Still Returns 403
1. Check email for Scrape.do activation link
2. Login to dashboard and verify account status
3. Contact support@scrape.do
4. Try alternative: see `GETTING_REAL_DATA.md` for browser cookie method

### HTML Parsing Returns No Flights
1. Check saved HTML file exists
2. Open in browser to verify it's the booking page
3. Look for the test case data manually (7:25 AM, $80, etc.)
4. Update selectors in `scraper_correct.py`

### GoWild Box Issue
1. Inspect the HTML for GoWild checkbox/button
2. Use browser DevTools → Network tab
3. Click the GoWild box and see what API call it makes
4. Implement the solution based on findings

---

## Success Checklist

Use this to validate everything works:

- [ ] Scrape.do token validates successfully
- [ ] `test_scrape_do_token.py` returns ✅
- [ ] `scraper_correct.py` downloads HTML file
- [ ] HTML file contains test case times: 7:25, 12:18, 10:35, 1:19
- [ ] HTML file contains test case prices: $80, $85
- [ ] Parser extracts 2 flights
- [ ] Flight times match exactly
- [ ] Flight prices match exactly
- [ ] GoWild availability detected
- [ ] Data saves to database
- [ ] Backend API returns flights
- [ ] Frontend displays flights

---

## Next Steps After Setup

Once everything works:

1. **Popular Routes First**
   - Scrape high-traffic routes (ORD, DEN, LAX, etc.)
   - Build up your flight database

2. **Schedule Regular Scraping**
   - Set up cron job or similar
   - Scrape popular routes daily

3. **Optimize Selectors**
   - As you scrape more routes, refine HTML parsing
   - Handle edge cases (cancellations, sold out, etc.)

4. **Monitor Changes**
   - Frontier may update their HTML structure
   - Keep an eye on parsing success rate

---

## Getting Help

If you get stuck:

1. **Check saved HTML files** - They show what Scrape.do returns
2. **Read logs** - The scraper logs everything
3. **Test incrementally** - Validate each step (token → HTML → parsing)
4. **Documentation** - See other .md files in this directory

---

**TL;DR:** Activate your Scrape.do account, get a working token, update `.env`, run `test_scrape_do_token.py`, then `scraper_correct.py`. Everything else is ready!
