"""
Frontier GoWild Flight Scraper using Scrape.do proxy service.

Scrape.do provides data center IPs that help bypass bot detection.
"""
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from typing import List, Dict, Optional
import json
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScapeDoScraper:
    """Scraper using Scrape.do proxy service."""

    def __init__(self):
        self.base_url = "https://www.flyfrontier.com"
        self.scrape_do_url = "http://api.scrape.do"

        if not settings.scrape_do_token:
            raise ValueError("Scrape.do API token not configured. Set SCRAPE_DO_TOKEN in .env")

    def build_scrape_do_url(self, target_url: str) -> str:
        """Build Scrape.do proxy URL."""
        from urllib.parse import quote
        encoded_url = quote(target_url, safe='')
        return f"{self.scrape_do_url}?token={settings.scrape_do_token}&url={encoded_url}"

    async def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str
    ) -> List[Dict]:
        """
        Search for flights using Scrape.do.

        Args:
            origin: Origin airport code (e.g., 'DEN')
            destination: Destination airport code (e.g., 'LAX')
            departure_date: Departure date in YYYY-MM-DD format

        Returns:
            List of flight dictionaries
        """
        logger.info(f"🔍 Searching: {origin} -> {destination} on {departure_date}")

        # Build Frontier search URL
        search_url = f"{self.base_url}/flight/select"
        search_url += f"?tripType=OW"
        search_url += f"&origin={origin}"
        search_url += f"&destination={destination}"
        search_url += f"&departureDate={departure_date}"
        search_url += f"&numAdults=1&numChildren=0"

        logger.info(f"Target URL: {search_url}")

        # Build Scrape.do proxy URL
        proxy_url = self.build_scrape_do_url(search_url)

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                logger.info("Making request through Scrape.do...")
                response = await client.get(proxy_url)

                logger.info(f"Response status: {response.status_code}")

                if response.status_code != 200:
                    logger.error(f"❌ Failed with status {response.status_code}")
                    logger.error(f"Response: {response.text[:500]}")
                    return []

                # Save HTML for debugging
                html_file = f"scraped_{origin}_{destination}_{departure_date}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                logger.info(f"✅ Saved HTML to {html_file}")

                # Parse flights
                flights = await self.parse_flights(
                    response.text,
                    origin,
                    destination,
                    departure_date
                )

                logger.info(f"✅ Found {len(flights)} flights")
                return flights

        except Exception as e:
            logger.error(f"❌ Error during scraping: {e}")
            import traceback
            traceback.print_exc()
            return []

    async def parse_flights(
        self,
        html_content: str,
        origin: str,
        destination: str,
        date: str
    ) -> List[Dict]:
        """
        Parse flight data from HTML.

        This method extracts flight information from Frontier's HTML.
        Update the selectors based on the actual HTML structure.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        flights = []

        logger.info("📄 Parsing HTML...")

        # Check page title
        title = soup.find('title')
        logger.info(f"Page title: {title.text if title else 'None'}")

        # Strategy 1: Look for JSON data in script tags
        scripts = soup.find_all('script')
        for script in scripts:
            if not script.string:
                continue

            # Look for JSON data
            if 'flight' in script.string.lower() and '{' in script.string:
                try:
                    # Try to find JSON objects
                    text = script.string
                    # Look for patterns like: var flightData = {...}
                    if 'var ' in text or 'const ' in text or 'let ' in text:
                        logger.info("Found potential flight data in JavaScript")
                        # You would parse this based on the actual structure
                except Exception as e:
                    logger.debug(f"Could not parse script: {e}")

        # Strategy 2: Look for common HTML patterns
        # These selectors are examples and need to be updated based on actual HTML

        # Look for flight cards/containers
        flight_containers = soup.find_all(['div', 'article'], class_=lambda x: x and any(
            keyword in str(x).lower() for keyword in ['flight', 'fare', 'card', 'option']
        ))

        logger.info(f"Found {len(flight_containers)} potential flight containers")

        for container in flight_containers:
            try:
                # Extract flight information
                # NOTE: These selectors are PLACEHOLDERS - update based on actual HTML!

                flight_data = {
                    'flight_number': 'F9-UNKNOWN',
                    'origin': origin,
                    'destination': destination,
                    'departure_date': date,
                    'departure_time': 'TBD',
                    'arrival_date': date,
                    'arrival_time': 'TBD',
                    'gowild_price': None,
                    'regular_price': None,
                    'is_gowild_available': False,
                    'duration': None,
                    'stops': 0,
                    'aircraft': None,
                }

                # Try to find times
                times = container.find_all('time')
                if len(times) >= 2:
                    flight_data['departure_time'] = times[0].text.strip()
                    flight_data['arrival_time'] = times[1].text.strip()

                # Try to find prices
                price_elements = container.find_all(text=lambda t: t and '$' in str(t))
                for price_text in price_elements:
                    try:
                        price = float(price_text.strip().replace('$', '').replace(',', ''))
                        # Heuristic: GoWild prices are usually under $5
                        if price < 5:
                            flight_data['gowild_price'] = price
                            flight_data['is_gowild_available'] = True
                        elif not flight_data['regular_price'] or price < flight_data['regular_price']:
                            flight_data['regular_price'] = price
                    except:
                        pass

                # Only add if we found meaningful data
                if flight_data['departure_time'] != 'TBD' or flight_data['gowild_price']:
                    flights.append(flight_data)

            except Exception as e:
                logger.warning(f"Error parsing flight container: {e}")
                continue

        # If no flights found, analyze structure
        if not flights:
            logger.warning("⚠️  No flights parsed - HTML structure analysis needed")
            self._analyze_html_structure(soup)

        return flights

    def _analyze_html_structure(self, soup: BeautifulSoup):
        """Analyze HTML to help identify correct selectors."""
        logger.info("\n" + "="*60)
        logger.info("HTML STRUCTURE ANALYSIS")
        logger.info("="*60)

        # Look for elements with 'gowild' or 'GoWild'
        gowild_elements = soup.find_all(text=lambda t: t and 'gowild' in str(t).lower())
        logger.info(f"\n'GoWild' mentions: {len(gowild_elements)}")
        if gowild_elements:
            for elem in gowild_elements[:3]:
                logger.info(f"  - {str(elem)[:100]}")

        # Look for price indicators
        price_elements = soup.find_all(text=lambda t: t and '$' in str(t))
        logger.info(f"\nPrice elements: {len(price_elements)}")
        if price_elements:
            for elem in price_elements[:5]:
                logger.info(f"  - {str(elem).strip()[:50]}")

        # Look for time elements
        time_elements = soup.find_all('time')
        logger.info(f"\nTime elements: {len(time_elements)}")

        # Look for common class patterns
        all_divs = soup.find_all('div', class_=True)
        class_patterns = {}
        for div in all_divs:
            classes = ' '.join(div.get('class', []))
            for keyword in ['flight', 'fare', 'price', 'time', 'card', 'option']:
                if keyword in classes.lower():
                    class_patterns[keyword] = class_patterns.get(keyword, 0) + 1

        logger.info("\nClass name patterns:")
        for keyword, count in sorted(class_patterns.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {keyword}: {count} elements")

        logger.info("="*60 + "\n")


async def test_scraper():
    """Test the Scrape.do scraper."""
    from datetime import timedelta

    scraper = ScapeDoScraper()

    # Test with tomorrow's date
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    logger.info("\n" + "="*60)
    logger.info("TESTING SCRAPE.DO INTEGRATION")
    logger.info("="*60 + "\n")

    flights = await scraper.search_flights('DEN', 'LAX', tomorrow)

    logger.info(f"\n{'='*60}")
    logger.info(f"RESULTS: Found {len(flights)} flights")
    logger.info("="*60)

    for i, flight in enumerate(flights, 1):
        logger.info(f"\nFlight {i}:")
        logger.info(f"  Route: {flight['origin']} → {flight['destination']}")
        logger.info(f"  Date: {flight['departure_date']}")
        logger.info(f"  Times: {flight['departure_time']} - {flight['arrival_time']}")
        if flight['is_gowild_available']:
            logger.info(f"  GoWild: ${flight['gowild_price']}")
        logger.info(f"  Regular: ${flight['regular_price']}" if flight['regular_price'] else "  Regular: N/A")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_scraper())
