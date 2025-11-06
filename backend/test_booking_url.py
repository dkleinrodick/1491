"""
Test the Frontier booking URL directly (without Scrape.do).
This will likely get blocked, but we can see what kind of response we get.
"""
import httpx
import asyncio
from datetime import datetime

async def test_direct_access():
    """Test direct access to Frontier booking page."""

    # Build URL for known test case: ORD -> CUN on 11/8/2025
    booking_url = "https://booking.flyfrontier.com/Flight/InternalSelect"
    booking_url += "?o1=ORD"
    booking_url += "&d1=CUN"
    booking_url += "&dd1=11-08-2025"
    booking_url += "&ADT=1"
    booking_url += "&mon=true"
    booking_url += "&promo="

    print("="*80)
    print("TESTING DIRECT ACCESS TO FRONTIER BOOKING")
    print("="*80)
    print(f"\nURL: {booking_url}")
    print("\nExpected flights (from user):")
    print("  1. 7:25 AM ORD -> 12:18 PM CUN (3h 53m, Nonstop, $80)")
    print("  2. 10:35 AM ATL -> 1:19 PM CUN (6h 19m, 1 Stop ATL, $85)")
    print("\n" + "="*80 + "\n")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            print("Making direct request...")
            response = await client.get(booking_url, headers=headers)

            print(f"Status Code: {response.status_code}")
            print(f"Final URL: {response.url}")
            print(f"Response length: {len(response.text)} characters")

            if response.status_code == 200:
                print("\n✅ Got 200 OK response!")

                # Save HTML
                with open('direct_booking_test.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("✅ Saved to direct_booking_test.html")

                # Quick analysis
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                title = soup.find('title')
                print(f"\nPage Title: {title.text if title else 'None'}")

                # Look for test case times
                test_times = ['7:25', '12:18', '10:35', '1:19']
                for time in test_times:
                    found = soup.find_all(text=lambda t: t and time in str(t))
                    print(f"  '{time}': {'✅ Found' if found else '❌ Not found'}")

            elif response.status_code == 403:
                print("\n❌ 403 Forbidden - Bot detection active")
                print("This confirms we need a proxy service like Scrape.do")

            else:
                print(f"\n⚠️  Got status {response.status_code}")
                print(f"Response preview: {response.text[:500]}")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_direct_access())
