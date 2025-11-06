"""
Test if your browser cookies work for accessing Frontier.

Usage:
1. Export cookies from your browser to cookies.json
2. Run: python test_cookies.py
"""
import json
import sys
import os

def test_cookies():
    """Test if cookies file exists and is valid."""

    print("🔍 Frontier Cookie Tester\n")

    # Check if cookies file exists
    if not os.path.exists('cookies.json'):
        print("❌ cookies.json not found!")
        print("\n📝 To create it:")
        print("1. Install Cookie-Editor extension in your browser")
        print("2. Go to flyfrontier.com and login")
        print("3. Click Cookie-Editor → Export → JSON")
        print("4. Save as 'cookies.json' in the backend/ folder")
        return False

    print("✅ cookies.json found")

    # Try to load and validate
    try:
        with open('cookies.json', 'r') as f:
            cookies = json.load(f)

        if not isinstance(cookies, list):
            print("❌ cookies.json should be a JSON array")
            return False

        print(f"✅ Loaded {len(cookies)} cookies")

        # Check for Frontier-specific cookies
        domains = set(c.get('domain', '') for c in cookies)
        frontier_cookies = [c for c in cookies if 'frontier' in c.get('domain', '').lower()]

        print(f"✅ Found {len(frontier_cookies)} Frontier cookies")

        if not frontier_cookies:
            print("⚠️  Warning: No Frontier-specific cookies found")
            print("   Make sure you exported cookies while on flyfrontier.com")

        # Show sample
        print("\n📋 Domains found:")
        for domain in sorted(domains):
            count = len([c for c in cookies if c.get('domain') == domain])
            print(f"   {domain}: {count} cookies")

        # Check for authentication cookies
        auth_cookies = [c for c in cookies if any(keyword in c.get('name', '').lower()
                       for keyword in ['session', 'auth', 'token', 'login'])]

        if auth_cookies:
            print(f"\n✅ Found {len(auth_cookies)} authentication cookies")
        else:
            print("\n⚠️  Warning: No authentication cookies found")
            print("   Make sure you're logged into your Frontier Miles account")

        print("\n✅ Cookie file looks good!")
        print("\n🚀 Next step: Run the scraper:")
        print("   python scraper_with_cookies.py")

        return True

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in cookies.json: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading cookies: {e}")
        return False


if __name__ == "__main__":
    success = test_cookies()
    sys.exit(0 if success else 1)
