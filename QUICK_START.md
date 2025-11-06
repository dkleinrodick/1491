# ⚡ QUICK START - Run This on Your Windows Computer

**Total time: ~20 minutes**

---

## Step 1: Install Python (5 min)

1. Go to https://www.python.org/downloads/
2. Click **"Download Python"**
3. Run the installer
4. ⚠️ **CHECK THE BOX: "Add Python to PATH"**
5. Click **"Install Now"**

---

## Step 2: Install Node.js (5 min)

1. Go to https://nodejs.org/
2. Click the **LTS** button (left side)
3. Run the installer
4. Click **"Next"** → **"Next"** → **"Install"**

---

## Step 3: Download the Code (2 min)

1. Go to https://github.com/dkleinrodick/1491
2. Click green **"Code"** button → **"Download ZIP"**
3. Extract the ZIP to your **Documents** folder
4. Rename the folder to just `1491`

---

## Step 4: Set Up Backend (5 min)

1. Open the `1491` folder
2. Open the `backend` folder
3. Click in the address bar (top of window)
4. Type: `cmd` and press Enter

In the black window that opens, type these commands **one at a time**:

```bash
python -m venv venv
```
Wait for it to finish, then:

```bash
venv\Scripts\activate
```
You should see `(venv)` appear. Then:

```bash
pip install -r requirements.txt
```
Wait 2-3 minutes for this to finish.

**Keep this window open!**

---

## Step 5: Set Up Frontend (3 min)

1. Open **another** File Explorer window
2. Go to `1491` → `frontend` folder
3. Click in the address bar
4. Type: `cmd` and press Enter

In this new black window, type:

```bash
npm install
```

Wait 2-3 minutes for this to finish.

**Keep this window open too!**

---

## Step 6: Run It! (1 min)

**In the FIRST window** (backend):
```bash
python main.py
```

**In the SECOND window** (frontend):
```bash
npm run dev
```

---

## Step 7: Open Your Browser

Go to: **http://localhost:5173**

**You should see your flight finder website!** ✅

---

## How to Use It

### See Test Flights
- The page loads with 6 sample flights already there

### Search Flights
- Enter airport codes (like `ORD` for Chicago, `LAX` for LA)
- Check "GoWild Only"
- Click "Search Flights"

### Scrape Real Flights
1. Open new tab: http://localhost:8000/docs
2. Find **POST /api/scrape/single-route**
3. Click **"Try it out"**
4. Enter:
   - origin: `ORD`
   - destination: `CUN`
   - date: `2025-11-08`
5. Click **"Execute"**
6. Wait 30-60 seconds
7. Go back to http://localhost:5173
8. Search for flights!

---

## When You're Done

In both black windows:
- Press **Ctrl+C**
- Type `y` and press Enter
- Close the windows

---

## Next Time You Want to Run It

**Backend window:**
```bash
cd Documents\1491\backend
venv\Scripts\activate
python main.py
```

**Frontend window:**
```bash
cd Documents\1491\frontend
npm run dev
```

**Browser:**
Go to http://localhost:5173

---

## Troubleshooting

**"python is not recognized"**
→ Reinstall Python, check "Add Python to PATH"

**"npm is not recognized"**
→ Reinstall Node.js

**403 Error when scraping**
→ Read `HOW_TO_ACTIVATE_SCRAPFLY.md`

**Need more help?**
→ Read `WINDOWS_SETUP_GUIDE.md` for detailed instructions

---

**That's it! You're running your own flight scraper!** 🎉
