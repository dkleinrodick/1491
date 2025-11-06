# Complete Windows Setup Guide for Beginners
## Frontier GoWild Flight Scraper

**For someone who knows nothing about coding!**

This guide assumes you're starting from scratch on Windows.

---

## Part 1: Install Required Software (30 minutes)

### Step 1: Install Python

**What is Python?** It's the programming language that runs the backend of your app.

1. **Download Python**
   - Go to: https://www.python.org/downloads/
   - Click the big yellow button: **"Download Python 3.11.x"**
   - Save the file (it's called something like `python-3.11.x-amd64.exe`)

2. **Install Python**
   - Double-click the downloaded file
   - ⚠️ **IMPORTANT:** Check the box that says **"Add Python to PATH"** at the bottom!
   - Click **"Install Now"**
   - Wait for installation to complete
   - Click **"Close"**

3. **Verify Python Installed**
   - Press `Windows Key + R`
   - Type: `cmd`
   - Press Enter
   - In the black window that opens, type: `python --version`
   - Press Enter
   - You should see: `Python 3.11.x`
   - If you see this, Python is installed! ✅
   - Close the window

---

### Step 2: Install Node.js

**What is Node.js?** It runs the frontend (the website part) of your app.

1. **Download Node.js**
   - Go to: https://nodejs.org/
   - Click the **"LTS"** button (the one on the left)
   - Save the file (called something like `node-v20.x.x-x64.msi`)

2. **Install Node.js**
   - Double-click the downloaded file
   - Click **"Next"** through all the screens
   - Accept the license agreement
   - Keep clicking **"Next"**
   - Click **"Install"**
   - Click **"Finish"**

3. **Verify Node.js Installed**
   - Press `Windows Key + R`
   - Type: `cmd`
   - Press Enter
   - Type: `node --version`
   - Press Enter
   - You should see: `v20.x.x`
   - Type: `npm --version`
   - Press Enter
   - You should see a number like `10.x.x`
   - If you see both, Node.js is installed! ✅
   - Close the window

---

### Step 3: Install Git (Optional but Recommended)

**What is Git?** It helps you download the code from GitHub.

1. **Download Git**
   - Go to: https://git-scm.com/download/win
   - The download should start automatically
   - Save the file (called something like `Git-2.x.x-64-bit.exe`)

2. **Install Git**
   - Double-click the downloaded file
   - Click **"Next"** through all screens (defaults are fine)
   - Click **"Install"**
   - Click **"Finish"**

3. **Verify Git Installed**
   - Press `Windows Key + R`
   - Type: `cmd`
   - Press Enter
   - Type: `git --version`
   - You should see: `git version 2.x.x`
   - Close the window

---

## Part 2: Download Your Code (10 minutes)

### Option A: Using Git (Recommended)

1. **Create a folder for your project**
   - Open **File Explorer** (Windows Key + E)
   - Go to your **Documents** folder
   - Right-click in empty space
   - Click **"New"** → **"Folder"**
   - Name it: `FrontierFlights`
   - Open the folder

2. **Open Command Prompt in this folder**
   - Click in the address bar at the top (where it shows the path)
   - Type: `cmd`
   - Press Enter
   - A black window opens - this is Command Prompt

3. **Download the code**
   - In the Command Prompt, type:
   ```
   git clone https://github.com/dkleinrodick/1491.git
   ```
   - Press Enter
   - Wait for download to complete
   - Type: `cd 1491`
   - Press Enter

### Option B: Download ZIP (If you didn't install Git)

1. **Download from GitHub**
   - Go to: https://github.com/dkleinrodick/1491
   - Click the green **"Code"** button
   - Click **"Download ZIP"**
   - Save the file

2. **Extract the ZIP**
   - Go to your **Downloads** folder
   - Right-click the `1491-main.zip` file
   - Click **"Extract All..."**
   - Click **"Extract"**
   - Open the extracted folder

3. **Open Command Prompt here**
   - Click in the address bar
   - Type: `cmd`
   - Press Enter

---

## Part 3: Set Up the Backend (15 minutes)

**What is the backend?** It's the server that scrapes flight data and stores it in a database.

### Step 1: Navigate to Backend Folder

In Command Prompt, type:
```
cd backend
```
Press Enter

### Step 2: Create Python Virtual Environment

Type:
```
python -m venv venv
```
Press Enter

Wait for it to finish (might take 1-2 minutes)

### Step 3: Activate Virtual Environment

Type:
```
venv\Scripts\activate
```
Press Enter

**You should now see `(venv)` at the beginning of your command line.** This means it worked! ✅

### Step 4: Install Python Packages

Type:
```
pip install -r requirements.txt
```
Press Enter

**This will take 3-5 minutes.** You'll see lots of text scrolling - that's normal!

Wait until you see something like `Successfully installed...` and the command prompt returns.

### Step 5: Verify Your API Key

1. Type:
   ```
   notepad .env
   ```
   Press Enter

2. A text file opens. Look for this line:
   ```
   SCRAPFLY_API_KEY=scp-live-c07f17fbff654e8188cd5308fa92018d
   ```

3. **If you got a DIFFERENT API key from Scrapfly**, replace the key here

4. Save the file (Ctrl+S)

5. Close Notepad

---

## Part 4: Set Up the Frontend (10 minutes)

**What is the frontend?** It's the website you'll use to search for flights.

### Step 1: Open New Command Prompt

1. Press `Windows Key + R`
2. Type: `cmd`
3. Press Enter

### Step 2: Navigate to Frontend Folder

Type (replace `USERNAME` with your Windows username):
```
cd C:\Users\USERNAME\Documents\FrontierFlights\1491\frontend
```
Press Enter

**Tip:** You can also navigate using File Explorer:
- Open the `1491` folder
- Open the `frontend` folder
- Click in the address bar
- Type: `cmd`
- Press Enter

### Step 3: Install Node Packages

Type:
```
npm install
```
Press Enter

**This will take 2-3 minutes.** You'll see lots of text - that's normal!

Wait for it to finish.

---

## Part 5: Run Your Application! (5 minutes)

Now you'll have **TWO Command Prompt windows** open:
- **Window 1**: Backend (in the `backend` folder)
- **Window 2**: Frontend (in the `frontend` folder)

### Start Backend (Window 1)

1. In the **first** Command Prompt (backend folder)
2. Make sure you see `(venv)` at the start
   - If not, type: `venv\Scripts\activate` and press Enter
3. Type:
   ```
   python main.py
   ```
4. Press Enter

**You should see:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**✅ Backend is running!** Don't close this window!

### Start Frontend (Window 2)

1. In the **second** Command Prompt (frontend folder)
2. Type:
   ```
   npm run dev
   ```
3. Press Enter

**You should see:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**✅ Frontend is running!** Don't close this window either!

---

## Part 6: Use Your Application!

### Open Your Browser

1. Open **Google Chrome**, **Firefox**, or **Edge**
2. Type in the address bar: `http://localhost:5173`
3. Press Enter

**You should see your Frontier GoWild Flight Finder website!** 🎉

---

## Part 7: How to Use It

### View Test Data

When you first open the site, you'll see **6 test flights** already loaded.

### Search for Flights

1. In the **Origin** box, type an airport code (like `ORD` for Chicago)
2. In the **Destination** box, type another airport code (like `CUN` for Cancun)
3. Check the **"GoWild Only"** box if you want only GoWild flights
4. Click **"Search Flights"**

You'll see the flights in the database for that route.

### Scrape a New Route

This is where the magic happens - you'll actually scrape live flight data!

**Using the Browser:**
1. Open a new tab
2. Go to: `http://localhost:8000/docs`
3. You'll see the **API Documentation** page
4. Scroll down to **POST /api/scrape/single-route**
5. Click **"Try it out"**
6. Fill in:
   - **origin**: `ORD`
   - **destination**: `CUN`
   - **date**: `2025-11-08`
7. Click **"Execute"**
8. Wait 30-60 seconds
9. Go back to http://localhost:5173
10. Search for ORD → CUN flights
11. You should see the newly scraped flights!

**Using Command Prompt (Advanced):**
1. Press `Windows Key + R`
2. Type: `cmd`
3. Press Enter
4. Type:
   ```
   curl -X POST "http://localhost:8000/api/scrape/single-route?origin=ORD&destination=CUN&date=2025-11-08"
   ```
5. Press Enter

---

## Part 8: Stopping the Application

When you're done:

1. Go to **Backend Command Prompt** (the first one)
2. Press **Ctrl+C**
3. Type: `y` if it asks to terminate
4. Press Enter

5. Go to **Frontend Command Prompt** (the second one)
6. Press **Ctrl+C**
7. Type: `y` if it asks to terminate
8. Press Enter

Both windows can now be closed.

---

## Part 9: Starting It Again Later

Next time you want to use your app:

### Start Backend:
1. Open Command Prompt
2. Navigate to backend folder:
   ```
   cd C:\Users\USERNAME\Documents\FrontierFlights\1491\backend
   ```
3. Activate virtual environment:
   ```
   venv\Scripts\activate
   ```
4. Start server:
   ```
   python main.py
   ```

### Start Frontend:
1. Open another Command Prompt
2. Navigate to frontend folder:
   ```
   cd C:\Users\USERNAME\Documents\FrontierFlights\1491\frontend
   ```
3. Start development server:
   ```
   npm run dev
   ```

### Open Browser:
Go to http://localhost:5173

---

## Troubleshooting

### Problem: "python is not recognized"

**Solution:**
- Python wasn't added to PATH during installation
- Reinstall Python, making sure to check **"Add Python to PATH"**

### Problem: "npm is not recognized"

**Solution:**
- Node.js wasn't installed correctly
- Reinstall Node.js

### Problem: "Cannot find module"

**Solution:**
- You might not be in the right folder
- Make sure you're in `backend` folder for backend commands
- Make sure you're in `frontend` folder for frontend commands

### Problem: Port already in use

**Solution:**
- Something else is using port 8000 or 5173
- Restart your computer
- Try again

### Problem: Backend starts but shows errors

**Solution:**
- Check your `.env` file has the correct API key
- Make sure you activated the virtual environment (you should see `(venv)`)

### Problem: 403 Forbidden when scraping

**Solution:**
- Your Scrapfly API key isn't activated yet
- Follow the steps in `HOW_TO_ACTIVATE_SCRAPFLY.md`
- Make sure you have credits in your Scrapfly account

### Problem: No flights show up

**Solution:**
- You're looking at an empty database
- Use the scrape endpoint to scrape some routes first
- Or the test data might not be loaded - check backend logs

---

## Video Tutorial Suggestion

If you prefer video instructions, search YouTube for:
- "How to run Python Flask API on Windows"
- "How to run React Vite app on Windows"
- "Installing Python on Windows 11"
- "Installing Node.js on Windows"

---

## File Locations Quick Reference

Replace `USERNAME` with your actual Windows username:

- **Project Root**: `C:\Users\USERNAME\Documents\FrontierFlights\1491\`
- **Backend Folder**: `C:\Users\USERNAME\Documents\FrontierFlights\1491\backend\`
- **Frontend Folder**: `C:\Users\USERNAME\Documents\FrontierFlights\1491\frontend\`
- **Config File**: `C:\Users\USERNAME\Documents\FrontierFlights\1491\backend\.env`
- **Database**: `C:\Users\USERNAME\Documents\FrontierFlights\1491\backend\gowild.db`

---

## Important URLs

While your app is running:

- **Frontend (Website)**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## What Each Folder Does

```
1491/
├── backend/                 ← Python server (scraping & database)
│   ├── main.py             ← Main server file
│   ├── scrapfly_scraper.py ← Flight scraper
│   ├── .env                ← Your API key is here
│   ├── gowild.db           ← Database with flights
│   └── venv/               ← Python virtual environment
│
├── frontend/                ← Website interface
│   ├── src/                ← React code
│   │   └── App.jsx         ← Main website component
│   └── node_modules/       ← Node.js packages
│
└── *.md                     ← Documentation files
```

---

## Need More Help?

If you get stuck:

1. **Read the error message** - it often tells you what's wrong
2. **Check you're in the right folder** - most errors come from this
3. **Make sure both backend AND frontend are running** - you need both
4. **Restart everything** - close all Command Prompts and start fresh
5. **Check the other guides** in the project folder for more details

---

## Success Checklist

- [ ] Python installed (type `python --version` in cmd)
- [ ] Node.js installed (type `node --version` in cmd)
- [ ] Code downloaded to Documents/FrontierFlights/1491
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] API key in .env file
- [ ] Backend running (see "Uvicorn running on...")
- [ ] Frontend running (see "Local: http://localhost:5173")
- [ ] Website opens in browser at http://localhost:5173
- [ ] Can see test flights on the website
- [ ] Can scrape a route (ORD → CUN test)

If you can check all these boxes, you're good to go! 🎉

---

**Bottom Line:**
1. Install Python and Node.js
2. Download the code
3. Run `pip install -r requirements.txt` in backend folder
4. Run `npm install` in frontend folder
5. Start backend with `python main.py`
6. Start frontend with `npm run dev`
7. Open http://localhost:5173 in your browser

That's it! You're now running a live flight scraper on your computer!
