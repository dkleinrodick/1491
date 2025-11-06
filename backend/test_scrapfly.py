"""Test Scrapfly API key and basic functionality."""
import asyncio
from scrapfly import ScrapflyClient, ScrapeConfig
from config import settings

async def test_api_key():
    """Test if Scrapfly API key is valid."""
    print("=" * 80)
    print("Testing Scrapfly API Key")
    print("=" * 80)
    print(f"\nAPI Key: {settings.scrapfly_api_key[:20]}...{settings.scrapfly_api_key[-10:]}")

    client = ScrapflyClient(key=settings.scrapfly_api_key)

    # Test with a simple URL first
    test_url = "https://httpbin.org/ip"
    print(f"\n1. Testing with simple URL: {test_url}")

    try:
        result = client.scrape(
            ScrapeConfig(
                url=test_url,
                render_js=False
            )
        )
        print(f"✅ Basic scraping works!")
        print(f"Response length: {len(result.content)} bytes")
        print(f"Status code: {result.status_code}")
    except Exception as e:
        print(f"❌ Basic scraping failed: {e}")
        return False

    # Test with JavaScript rendering
    print(f"\n2. Testing JavaScript rendering...")
    try:
        result = client.scrape(
            ScrapeConfig(
                url=test_url,
                render_js=True
            )
        )
        print(f"✅ JavaScript rendering works!")
    except Exception as e:
        print(f"❌ JavaScript rendering failed: {e}")
        return False

    # Test with Frontier URL (simple parameters)
    print(f"\n3. Testing Frontier URL without GoWild...")
    frontier_url = "https://booking.flyfrontier.com/Flight/InternalSelect?o1=ORD&d1=LAX&dd1=2025-11-09&adt=1"

    try:
        result = client.scrape(
            ScrapeConfig(
                url=frontier_url,
                render_js=True,
                wait_for_selector='.ibe-flight-info',
                timeout=30000
            )
        )
        print(f"✅ Frontier URL works!")
        print(f"Response length: {len(result.content)} bytes")

        # Check if we got the booking page
        if 'flight' in result.content.lower():
            print(f"✅ Page contains flight data")

    except Exception as e:
        print(f"❌ Frontier URL failed: {e}")
        return False

    # Test with GoWild parameter
    print(f"\n4. Testing Frontier URL WITH GoWild (ftype=GW)...")
    gowild_url = "https://booking.flyfrontier.com/Flight/InternalSelect?o1=ORD&d1=LAX&dd1=2025-11-09&adt=1&ftype=GW"

    try:
        result = client.scrape(
            ScrapeConfig(
                url=gowild_url,
                render_js=True,
                wait_for_selector='.ibe-flight-info',
                timeout=30000
            )
        )
        print(f"✅ GoWild URL works!")
        print(f"Response length: {len(result.content)} bytes")

        # Save for inspection
        with open('frontier_gowild_test.html', 'w', encoding='utf-8') as f:
            f.write(result.content)
        print(f"💾 Saved to frontier_gowild_test.html")

    except Exception as e:
        print(f"❌ GoWild URL failed: {e}")
        return False

    print(f"\n" + "=" * 80)
    print(f"✅ All tests passed!")
    print(f"=" * 80)
    return True

if __name__ == "__main__":
    asyncio.run(test_api_key())
