"""Test Scrapfly API directly with requests."""
import requests
from config import settings

def test_scrapfly_direct():
    """Test Scrapfly API with direct HTTP request."""
    print("=" * 80)
    print("Testing Scrapfly API (Direct HTTP)")
    print("=" * 80)

    api_key = settings.scrapfly_api_key
    print(f"\nAPI Key: {api_key[:20]}...{api_key[-10:]}")

    # Test endpoint
    test_url = "https://httpbin.org/ip"

    # Scrapfly API endpoint
    scrapfly_url = f"https://api.scrapfly.io/scrape"

    params = {
        'key': api_key,
        'url': test_url
    }

    print(f"\nTesting simple request to: {test_url}")
    print(f"Scrapfly API: {scrapfly_url}")

    try:
        response = requests.get(scrapfly_url, params=params, timeout=30)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            print(f"✅ API Key is VALID!")
            print(f"Response (first 500 chars):\n{response.text[:500]}")
            return True
        elif response.status_code == 403:
            print(f"❌ 403 Forbidden - API key invalid or account not activated")
            print(f"Response: {response.text[:500]}")
            return False
        elif response.status_code == 401:
            print(f"❌ 401 Unauthorized - API key missing or invalid")
            print(f"Response: {response.text[:500]}")
            return False
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False

    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    test_scrapfly_direct()
