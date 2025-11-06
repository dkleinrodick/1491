"""
Frontier GoWild scraper with CORRECT Scrape.do integration.

Based on official Scrape.do documentation:
https://scrape.do/documentation/
"""
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from typing import List, Dict
from urllib.parse import quote
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScrapeDoCorrected:
    """Scraper using correct Scrape.do API format."""

    def __init__(self):
        self.scrape_do_api = "https://api.scrape.do/"
        self.booking_url_base = "https://booking.flyfrontier.com/Flight/InternalSelect"

        if not settings.scrape_do_token:
            raise ValueError("Scrape.do API token not configured. Set SCRAPE_DO_TOKEN in .env")

    def build_booking_url(self, origin: str, destination: str, date_str: str) -> str:
        """
        Build the Frontier booking URL.

        Args:
            origin: Origin airport code (e.g., 'ORD')
            destination: Destination airport code (e.g., 'CUN')
            date_str: Date in YYYY-MM-DD format

        Returns:
            Complete booking URL
        """
        # Convert YYYY-MM-DD to MM-DD-YYYY
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        frontier_date = date_obj.strftime('%m-%d-%Y')

        url = f"{self.booking_url_base}?"
        url += f"o1={origin.upper()}"
        url += f"&d1={destination.upper()}"
        url += f"&dd1={frontier_date}"
        url += f"&ADT=1"
        url += f"&mon=true"
        url += f"&promo="

        return url

    def build_scrape_do_request_url(
        self,
        target_url: str,
        render: bool = True,
        custom_wait: int = 3000
    ) -> str:
        """
        Build correct Scrape.do API request URL.

        Format: https://api.scrape.do/?token=YOUR_TOKEN&url=TARGET_URL

        Args:
            target_url: The target website URL to scrape
            render: Use headless browser to render JavaScript (default True)
            custom_wait: Wait time in milliseconds after page load (default 3000)

        Returns:
            Complete Scrape.do API URL
        """
        # URL encode the target URL
        encoded_url = quote(target_url, safe='')

        # Build Scrape.do API URL with parameters
        api_url = f"{self.scrape_do_api}?"
        api_url += f"token={settings.scrape_do_token}"
        api_url += f"&url={encoded_url}"

        if render:
            api_url += "&render=true"
            api_url += f"&customWait={custom_wait}"
            # Block resources to speed up and reduce costs
            api_url += "&blockResources=true"

        return api_url

    async def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        render_js: bool = True
    ) -> List[Dict]:
        """
        Search for flights using Scrape.do.

        Args:
            origin: Origin airport code (e.g., 'ORD')
            destination: Destination airport code (e.g., 'CUN')
            departure_date: Date in YYYY-MM-DD format
            render_js: Use headless browser to render JavaScript (default True)

        Returns:
            List of flight dictionaries
        """
        logger.info(f"🔍 Searching: {origin} -> {destination} on {departure_date}")

        # Build Frontier booking URL
        booking_url = self.build_booking_url(origin, destination, departure_date)
        logger.info(f"Booking URL: {booking_url}")

        # Build Scrape.do API request URL
        scrape_do_url = self.build_scrape_do_request_url(
            booking_url,
            render=render_js,
            custom_wait=5000  # Wait 5 seconds for JS to load
        )

        logger.info(f"Scrape.do API URL: {scrape_do_url[:100]}...")

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                logger.info("Making request through Scrape.do API...")
                response = await client.get(scrape_do_url)

                logger.info(f"Response status: {response.status_code}")
                logger.info(f"Response size: {len(response.text)} bytes")

                if response.status_code != 200:
                    logger.error(f"❌ Failed with status {response.status_code}")
                    logger.error(f"Response: {response.text[:500]}")
                    return []

                # Save HTML for debugging
                html_file = f"frontier_{origin}_{destination}_{departure_date}.html"
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

        except httpx.TimeoutException:
            logger.error("❌ Request timed out")
            return []
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
        Parse flight data from Frontier booking page HTML.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        flights = []

        logger.info("📄 Parsing HTML...")

        # Check page title
        title = soup.find('title')
        logger.info(f"Page title: {title.text if title else 'None'}")

        # Look for test case data (ORD->CUN 11/8/25)
        test_times = ['7:25', '12:18', '10:35', '1:19']
        test_prices = ['$80', '$85']

        logger.info("\n🔍 Looking for test case data:")
        for test_time in test_times:
            found = soup.find_all(text=lambda t: t and test_time in str(t))
            if found:
                logger.info(f"  ✅ Found '{test_time}': {len(found)} occurrences")
            else:
                logger.info(f"  ❌ '{test_time}' not found")

        for test_price in test_prices:
            found = soup.find_all(text=lambda t: t and test_price in str(t))
            if found:
                logger.info(f"  ✅ Found '{test_price}': {len(found)} occurrences")

        # Look for GoWild-specific elements
        gowild_elements = soup.find_all(text=lambda t: t and 'gowild' in str(t).lower())
        logger.info(f"\n'GoWild' mentions: {len(gowild_elements)}")
        if gowild_elements:
            for elem in gowild_elements[:3]:
                logger.info(f"  {str(elem).strip()[:80]}")

        # Look for flight containers
        # Common selectors for booking pages
        potential_selectors = [
            'div[class*="flight"]',
            'div[class*="fare"]',
            'div[class*="option"]',
            '[data-test*="flight"]',
            '.flight-card',
            '.fare-option',
            'article',
        ]

        all_containers = []
        for selector in potential_selectors:
            containers = soup.select(selector)
            if containers:
                logger.info(f"Found {len(containers)} elements with selector: {selector}")
                all_containers.extend(containers)

        # Remove duplicates
        all_containers = list(set(all_containers))
        logger.info(f"\nTotal unique flight containers: {len(all_containers)}")

        # Parse each container
        for i, container in enumerate(all_containers[:20], 1):
            try:
                flight_data = {
                    'flight_number': 'F9-UNKNOWN',
                    'origin': origin,
                    'destination': destination,
                    'departure_date': date,
                    'departure_time': None,
                    'arrival_date': date,
                    'arrival_time': None,
                    'gowild_price': None,
                    'regular_price': None,
                    'is_gowild_available': False,
                    'duration': None,
                    'stops': 0,
                    'aircraft': None,
                }

                # Extract times (look for AM/PM patterns)
                time_pattern = soup.find_all(text=lambda t: t and ':' in str(t) and (
                    'AM' in str(t).upper() or 'PM' in str(t).upper()
                ))
                times_in_container = [t for t in time_pattern if t in container.get_text()]

                if len(times_in_container) >= 2:
                    flight_data['departure_time'] = times_in_container[0].strip()
                    flight_data['arrival_time'] = times_in_container[1].strip()

                # Extract prices
                price_texts = container.find_all(text=lambda t: t and '$' in str(t))
                for price_text in price_texts:
                    try:
                        price_str = price_text.strip().replace('$', '').replace(',', '').split()[0]
                        price = float(price_str)
                        if price < 1000:  # Reasonable price
                            if not flight_data['regular_price'] or price < flight_data['regular_price']:
                                flight_data['regular_price'] = price

                            # Check if this is a GoWild price
                            # GoWild prices are typically very low ($0.99-$5)
                            # But test case shows $80-$85 which might be regular prices
                            if price < 5:
                                flight_data['gowild_price'] = price
                                flight_data['is_gowild_available'] = True
                    except:
                        pass

                # Extract duration
                duration_text = container.find(text=lambda t: t and 'hrs' in str(t).lower() or 'min' in str(t).lower())
                if duration_text:
                    flight_data['duration'] = duration_text.strip()

                # Extract stops
                stop_text = container.find(text=lambda t: t and 'stop' in str(t).lower())
                if stop_text:
                    if 'nonstop' in stop_text.lower():
                        flight_data['stops'] = 0
                    else:
                        import re
                        match = re.search(r'(\d+)\s*stop', stop_text.lower())
                        if match:
                            flight_data['stops'] = int(match.group(1))

                # Only add if we have meaningful data
                if flight_data['departure_time'] and flight_data['arrival_time']:
                    flights.append(flight_data)
                    logger.info(f"  Parsed flight {i}: {flight_data['departure_time']} -> {flight_data['arrival_time']}")

            except Exception as e:
                logger.debug(f"Error parsing container {i}: {e}")

        if not flights:
            logger.warning("\n⚠️  No flights parsed - analyzing HTML structure...")
            self._analyze_html(soup, origin, destination)

        return flights

    def _analyze_html(self, soup: BeautifulSoup, origin: str, destination: str):
        """Detailed HTML analysis for debugging."""
        logger.info("\n" + "="*80)
        logger.info("HTML STRUCTURE ANALYSIS")
        logger.info("="*80)

        # Check for common elements
        logger.info(f"\nPage Statistics:")
        logger.info(f"  Total divs: {len(soup.find_all('div'))}")
        logger.info(f"  Total scripts: {len(soup.find_all('script'))}")
        logger.info(f"  Total buttons: {len(soup.find_all('button'))}")
        logger.info(f"  Total inputs: {len(soup.find_all('input'))}")

        # Look for GoWild-related elements
        gowild_classes = soup.find_all(class_=lambda x: x and 'gowild' in str(x).lower())
        gowild_ids = soup.find_all(id=lambda x: x and 'gowild' in str(x).lower())

        logger.info(f"\nGoWild Elements:")
        logger.info(f"  Classes with 'gowild': {len(gowild_classes)}")
        logger.info(f"  IDs with 'gowild': {len(gowild_ids)}")

        if gowild_classes:
            for elem in gowild_classes[:3]:
                logger.info(f"    {elem.name}.{elem.get('class')}")

        # Look for checkboxes/buttons (the GoWild box the user mentioned)
        checkboxes = soup.find_all('input', type='checkbox')
        logger.info(f"\n  Checkboxes found: {len(checkboxes)}")
        for cb in checkboxes[:5]:
            logger.info(f"    {cb.get('id', 'no-id')} - {cb.get('name', 'no-name')}")

        # Look for data attributes
        data_attrs = soup.find_all(attrs=lambda x: x and any(k.startswith('data-') for k in x.keys()))
        logger.info(f"\n  Elements with data- attributes: {len(data_attrs)}")

        logger.info("="*80 + "\n")


async def test_correct_integration():
    """Test with correct Scrape.do integration."""
    logger.info("="*80)
    logger.info("TESTING CORRECT SCRAPE.DO INTEGRATION")
    logger.info("="*80)
    logger.info("\nTest Case: ORD -> CUN on 11/8/2025")
    logger.info("Expected Results:")
    logger.info("  Flight 1: 7:25 AM ORD -> 12:18 PM CUN (3h 53m, Nonstop, $80)")
    logger.info("  Flight 2: 10:35 AM ATL -> 1:19 PM CUN (6h 19m, 1 Stop, $85)")
    logger.info("="*80 + "\n")

    scraper = ScrapeDoCorrected()

    # Test with known data
    flights = await scraper.search_flights('ORD', 'CUN', '2025-11-08', render_js=True)

    logger.info(f"\n{'='*80}")
    logger.info(f"RESULTS: Found {len(flights)} flights")
    logger.info("="*80)

    if flights:
        for i, flight in enumerate(flights, 1):
            logger.info(f"\nFlight {i}:")
            logger.info(f"  Route: {flight['origin']} → {flight['destination']}")
            logger.info(f"  Times: {flight['departure_time']} -> {flight['arrival_time']}")
            logger.info(f"  Duration: {flight['duration']}")
            logger.info(f"  Stops: {flight['stops']}")
            logger.info(f"  Price: ${flight['regular_price']}" if flight['regular_price'] else "  Price: N/A")
            logger.info(f"  GoWild: {flight['is_gowild_available']}")

        # Validate against test case
        logger.info(f"\n{'='*80}")
        logger.info("VALIDATION")
        logger.info("="*80)

        if len(flights) == 2:
            logger.info("✅ Found expected 2 flights")
        else:
            logger.warning(f"⚠️  Expected 2 flights, found {len(flights)}")

        # Check for specific times
        times_found = [f['departure_time'] for f in flights if f['departure_time']]
        expected_times = ['7:25 AM', '10:35 AM']
        for expected in expected_times:
            if any(expected in str(t) for t in times_found):
                logger.info(f"✅ Found expected time: {expected}")
            else:
                logger.warning(f"⚠️  Expected time not found: {expected}")

    else:
        logger.warning("\n⚠️  No flights parsed!")
        logger.warning(f"Check saved HTML: frontier_ORD_CUN_2025-11-08.html")

    logger.info("\n" + "="*80)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_correct_integration())
