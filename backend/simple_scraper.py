"""
Simple HTTP-based scraper for Frontier Airlines.
Uses requests instead of Playwright to work in restricted environments.
"""
import httpx
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import random
from typing import List, Dict

class SimpleFrontierScraper:
    """Simple scraper using HTTP requests."""

    def __init__(self):
        self.base_url = "https://www.flyfrontier.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }

    def search_flights(self, origin: str, destination: str, departure_date: str) -> List[Dict]:
        """Search for flights using HTTP requests."""
        print(f"Searching: {origin} -> {destination} on {departure_date}")

        # Try the booking URL
        search_url = f"{self.base_url}/flight/select"
        params = {
            'tripType': 'OW',
            'origin': origin,
            'destination': destination,
            'departureDate': departure_date,
            'numAdults': '1',
            'numChildren': '0'
        }

        try:
            # Make request with timeout
            with httpx.Client(timeout=30.0, follow_redirects=True) as client:
                response = client.get(search_url, params=params, headers=self.headers)

                print(f"Status: {response.status_code}")

                if response.status_code == 403:
                    print("❌ Got 403 - Bot detection triggered")
                    return []

                if response.status_code != 200:
                    print(f"❌ Got status code {response.status_code}")
                    return []

                # Save response for debugging
                with open('frontier_response.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("✅ Saved response to frontier_response.html")

                # Parse the HTML
                soup = BeautifulSoup(response.text, 'html.parser')

                # Look for flight data
                # This is where we need to find the actual selectors
                flights = self.parse_flights(soup, origin, destination, departure_date)

                return flights

        except Exception as e:
            print(f"❌ Error: {e}")
            return []

    def parse_flights(self, soup: BeautifulSoup, origin: str, destination: str, date: str) -> List[Dict]:
        """Parse flight data from HTML."""
        flights = []

        # Look for common patterns
        print("\n🔍 Looking for flight data...")

        # Check if we got the booking page
        title = soup.find('title')
        print(f"Page title: {title.text if title else 'None'}")

        # Look for flight cards/containers
        possible_selectors = [
            'div[data-testid*="flight"]',
            'div[class*="flight"]',
            'div[class*="fare"]',
            'article',
            '.flight-card',
            '.booking-flight',
        ]

        for selector in possible_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"  Found {len(elements)} elements with selector: {selector}")

        # Look for JSON data (many sites embed data in scripts)
        scripts = soup.find_all('script')
        print(f"  Found {len(scripts)} script tags")

        for script in scripts:
            if script.string and 'flight' in script.string.lower():
                # Look for JSON data
                text = script.string[:200]  # First 200 chars
                if '{' in text:
                    print(f"  Found potential flight data in script tag")

        # For now, return empty - we need to inspect the actual HTML
        print("\n⚠️  Need to inspect HTML to find correct selectors")

        return flights


if __name__ == "__main__":
    scraper = SimpleFrontierScraper()

    # Test with a real search
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    flights = scraper.search_flights('DEN', 'LAX', tomorrow)

    print(f"\n{'='*50}")
    print(f"Found {len(flights)} flights")
