"""
Test using cloudscraper to bypass Cloudflare.
"""
import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def test_frontier_access():
    """Test accessing Frontier with cloudscraper."""

    # Create scraper
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        }
    )

    # Try to access Frontier homepage first
    print("Testing Frontier homepage...")
    try:
        response = scraper.get('https://www.flyfrontier.com')
        print(f"Homepage Status: {response.status_code}")

        if response.status_code == 200:
            print("✅ Successfully accessed homepage!")

            # Now try flight search
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            search_url = 'https://www.flyfrontier.com/flight/select'
            params = {
                'tripType': 'OW',
                'origin': 'DEN',
                'destination': 'LAX',
                'departureDate': tomorrow,
                'numAdults': '1',
                'numChildren': '0'
            }

            print(f"\nTrying flight search: DEN -> LAX on {tomorrow}...")
            response = scraper.get(search_url, params=params)
            print(f"Search Status: {response.status_code}")

            if response.status_code == 200:
                print("✅ Successfully accessed flight search!")

                # Save and analyze
                with open('frontier_search.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("✅ Saved to frontier_search.html")

                soup = BeautifulSoup(response.text, 'html.parser')

                # Look for flight data
                print("\n🔍 Analyzing page structure...")

                # Check title
                title = soup.find('title')
                print(f"Title: {title.text if title else 'None'}")

                # Look for specific elements
                flight_cards = soup.find_all(['div', 'article'], class_=lambda x: x and 'flight' in str(x).lower())
                print(f"Potential flight cards: {len(flight_cards)}")

                # Look for price elements
                prices = soup.find_all(text=lambda t: t and '$' in str(t))
                print(f"Found {len(prices)} price elements")
                if prices:
                    print(f"Sample prices: {[p.strip()[:30] for p in prices[:5]]}")

                # Look for JavaScript data
                scripts = soup.find_all('script')
                for i, script in enumerate(scripts):
                    if script.string and any(keyword in script.string.lower() for keyword in ['flight', 'booking', 'fare']):
                        print(f"\n📜 Script {i} might contain flight data (length: {len(script.string)})")
                        # Check if it's JSON
                        if '{' in script.string and 'flight' in script.string.lower():
                            print("   Contains JSON-like structure with 'flight' keyword")

            else:
                print(f"❌ Search failed with status: {response.status_code}")

        else:
            print(f"❌ Homepage access failed")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_frontier_access()
