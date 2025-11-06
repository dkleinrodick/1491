# How to Activate Your Scrapfly API Key

## Step-by-Step Guide

### Step 1: Go to Scrapfly Website
Open your browser and go to: **https://scrapfly.io/**

---

### Step 2: Sign Up or Login

#### Option A: If You Don't Have an Account Yet
1. Click **"Sign Up"** or **"Get Started Free"** button
2. Fill in your details:
   - Email address
   - Password
   - Company name (can be anything)
3. Click **"Create Account"**
4. **Check your email** for verification link
5. Click the verification link to activate your account

#### Option B: If You Already Have an Account
1. Click **"Login"** button
2. Enter your email and password
3. Click **"Sign In"**

---

### Step 3: Access Your Dashboard
Once logged in, you should see your dashboard at:
**https://scrapfly.io/dashboard**

---

### Step 4: Find Your API Key

1. Look for **"API Keys"** section in the dashboard
   - Usually in the sidebar or top menu
   - Or go directly to: **https://scrapfly.io/dashboard/api**

2. You should see your API key displayed

3. **Copy your API key** - it should look like:
   ```
   scp-live-xxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

### Step 5: Check Your Account Status

In the dashboard, verify:
- ✅ Account is **active** (not pending)
- ✅ You have **credits** or a **free trial**
- ✅ No payment issues or restrictions

**Free Trial Details:**
- Scrapfly typically offers **1,000 free API calls** when you sign up
- No credit card required for trial
- Perfect for testing!

---

### Step 6: Update Your .env File

If the API key in the dashboard is **different** from what we have:

```bash
cd /home/user/1491/backend
nano .env
```

Update line 26 with your **actual** API key from the dashboard:
```
SCRAPFLY_API_KEY=your-actual-key-from-dashboard
```

Save and exit (Ctrl+X, then Y, then Enter)

---

### Step 7: Test Your API Key

```bash
cd /home/user/1491/backend
source venv/bin/activate
python test_scrapfly_direct.py
```

**Expected Output (when working):**
```
✅ API Key is VALID!
Response: {...}
```

**If you still get 403:**
- Double-check you copied the key correctly (no extra spaces)
- Make sure account shows as "Active" in dashboard
- Verify you have available credits
- Try generating a **new API key** in the dashboard

---

## Troubleshooting

### Problem: Can't Find API Key Section

**Solution:**
1. Look for menu items like:
   - "API Keys"
   - "Settings"
   - "Integration"
   - "Credentials"
2. Or use the search box in the dashboard
3. Or go to: https://scrapfly.io/dashboard/api

---

### Problem: Account Says "Pending" or "Inactive"

**Solution:**
1. Check your email for verification link
2. Click the verification link
3. Wait a few minutes for activation
4. Refresh the dashboard page

---

### Problem: No Free Credits Available

**Solution:**
1. Check if you need to:
   - Verify your email
   - Complete account setup
   - Add a payment method (even for free trial)
2. Contact Scrapfly support if needed

---

### Problem: API Key Still Returns 403

**Solutions to try:**

#### 1. Generate a New API Key
1. Go to API Keys section in dashboard
2. Click **"Generate New Key"** or **"Create API Key"**
3. Copy the new key
4. Update your `.env` file with the new key
5. Test again

#### 2. Check API Key Format
- Should start with `scp-live-`
- Should be about 40-50 characters long
- No spaces before or after
- All lowercase

#### 3. Verify Account Limits
- Check if you've exceeded free trial limits
- Verify account status is "Active"
- Check if any restrictions are applied

#### 4. Contact Support
If nothing works, email: **support@scrapfly.io**

Tell them:
- You're getting 403 Forbidden errors
- Your API key: `scp-live-c07f17fbff654e8188cd5308fa92018d`
- You've verified account is active
- You need help activating the key

They usually respond within 24 hours.

---

## Alternative: Create a Fresh Account

If you're having trouble with the existing key, you can:

1. **Create a new account** at https://scrapfly.io/
2. Use a different email address
3. Get a **new API key** from the new account
4. Update `.env` with the new key

This gives you a fresh start with a guaranteed working key.

---

## Quick Checklist

Use this to make sure everything is set up:

- [ ] Went to https://scrapfly.io/
- [ ] Signed up or logged in
- [ ] Verified email address (check spam folder)
- [ ] Account shows as "Active" in dashboard
- [ ] Found API key in dashboard
- [ ] Copied API key (starts with `scp-live-`)
- [ ] Updated `.env` file with correct key
- [ ] Ran `python test_scrapfly_direct.py`
- [ ] Saw "✅ API Key is VALID!" message

---

## What the Dashboard Should Look Like

When you login, you should see:

```
Dashboard
├── Overview
│   ├── API Calls Used: 0 / 1000
│   ├── Account Status: Active
│   └── Credits Remaining: 1000
│
├── API Keys
│   └── Your Key: scp-live-xxxxxxxxxxxx
│       [Copy] [Regenerate] [Delete]
│
├── Usage
│   └── Recent API calls
│
└── Settings
    └── Account details
```

---

## After Activation

Once your key works (you see ✅ in the test), you can:

### 1. Test Full Scraper
```bash
python scrapfly_scraper.py
```

This will scrape the ORD→CUN test case.

### 2. Start Your Application
```bash
# Terminal 1: Backend
python main.py

# Terminal 2: Frontend
cd ../frontend
npm run dev
```

### 3. Use the API
```bash
# Scrape a route
curl -X POST "http://localhost:8000/api/scrape/single-route?origin=ORD&destination=CUN&date=2025-11-08"

# Get flights
curl "http://localhost:8000/api/flights?gowild_only=true"
```

---

## Common Scrapfly Account Issues

### Issue: Email Verification Required
- **Check your inbox** for verification email
- **Check spam/junk folder**
- Wait 5-10 minutes for email to arrive
- Use the "Resend verification" option if available

### Issue: Need Credit Card for Free Trial
- Some services require a card even for free trials
- **No charges** will be made during trial period
- You can cancel anytime before trial ends

### Issue: Account Region Restrictions
- Scrapfly is available worldwide
- If you see region restrictions, try:
  - Different email provider
  - VPN to different country
  - Contact support

---

## Support Contacts

If you need help:

- **Email**: support@scrapfly.io
- **Website**: https://scrapfly.io/
- **Documentation**: https://scrapfly.io/docs/
- **Status Page**: Check if Scrapfly is having issues

---

## Summary

**Quick Version:**
1. Go to https://scrapfly.io/
2. Sign up (use any email)
3. Verify your email
4. Go to dashboard → API Keys
5. Copy your API key
6. Update `.env` if different
7. Run `python test_scrapfly_direct.py`
8. Should see ✅ API Key is VALID!

That's it! Once you see ✅, everything will work.

---

## Need Help?

If you're stuck at any step:
1. Take a screenshot of what you see
2. Note any error messages
3. I can help troubleshoot further

The key thing is to get a **working API key** from an **activated Scrapfly account**. Once that's done, everything else is already built and ready to go!
