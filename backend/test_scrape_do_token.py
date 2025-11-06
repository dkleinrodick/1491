"""Test if Scrape.do token is valid."""
import httpx
import asyncio
from config import settings

async def test_token():
    """Test Scrape.do with a simple website."""

    print(f"Testing Scrape.do token...")
    print(f"Token (first 20 chars): {settings.scrape_do_token[:20]}...")
    print()

    # Test with httpbin.org (simple test site)
    test_url = "https://httpbin.org/ip"

    # Build Scrape.do URL
    from urllib.parse import quote
    encoded_url = quote(test_url, safe='')
    scrape_do_url = f"http://api.scrape.do?token={settings.scrape_do_token}&url={encoded_url}"

    print(f"Test URL: {test_url}")
    print(f"Scrape.do URL: {scrape_do_url[:80]}...")
    print()

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            print("Making request...")
            response = await client.get(scrape_do_url)

            print(f"\nStatus Code: {response.status_code}")
            print(f"Response: {response.text[:500]}")

            if response.status_code == 200:
                print("\n✅ Scrape.do token is WORKING!")
            elif response.status_code == 403:
                print("\n❌ 403 Forbidden - Token may be invalid or account inactive")
                print("   Check:")
                print("   1. Token is correct")
                print("   2. Scrape.do account is active")
                print("   3. Account has credits")
            else:
                print(f"\n⚠️  Unexpected status: {response.status_code}")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_token())
