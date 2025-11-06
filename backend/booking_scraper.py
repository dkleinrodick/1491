"""
Updated Frontier GoWild scraper using the correct booking URL.

URL structure: https://booking.flyfrontier.com/Flight/InternalSelect
Parameters:
- o1: Origin airport code (e.g., ORD)
- d1: Destination airport code (e.g., LAX)
- dd1: Date in MM-DD-YYYY format (e.g., 11-06-2025)
- ADT: Number of adults (1)
- mon: true
- promo: (empty)
"""
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from typing import List, Dict
import json
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FrontierBookingScraper:
    """Scraper using the correct Frontier booking URL."""

    def __init__(self):
        self.booking_url = "https://booking.flyfrontier.com/Flight/InternalSelect"

    def build_booking_url(self, origin: str, destination: str, date_str: str) -> str:
        """
        Build the Frontier booking URL.

        Args:
            origin: Origin airport code (e.g., 'ORD')
            destination: Destination airport code (e.g., 'LAX')
            date_str: Date in YYYY-MM-DD format

        Returns:
            Complete booking URL
        """
        # Convert YYYY-MM-DD to MM-DD-YYYY
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        frontier_date = date_obj.strftime('%m-%d-%Y')

        url = f"{self.booking_url}?"
        url += f"o1={origin.upper()}"
        url += f"&d1={destination.upper()}"
        url += f"&dd1={frontier_date}"
        url += f"&ADT=1"
        url += f"&mon=true"
        url += f"&promo="

        return url

    def build_scrape_do_url(self, target_url: str) -> str:
        """Build Scrape.do proxy URL."""
        if not settings.scrape_do_token:
            raise ValueError("Scrape.do token not configured")

        from urllib.parse import quote
        encoded_url = quote(target_url, safe='')
        return f"http://api.scrape.do?token={settings.scrape_do_token}&url={encoded_url}"

    async def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str
    ) -> List[Dict]:
        """
        Search for flights using Scrape.do.

        Args:
            origin: Origin airport code (e.g., 'ORD')
            destination: Destination airport code (e.g., 'CUN')
            departure_date: Date in YYYY-MM-DD format

        Returns:
            List of flight dictionaries
        """
        logger.info(f"🔍 Searching: {origin} -> {destination} on {departure_date}")

        # Build Frontier booking URL
        booking_url = self.build_booking_url(origin, destination, departure_date)
        logger.info(f"Booking URL: {booking_url}")

        # Build Scrape.do proxy URL
        proxy_url = self.build_scrape_do_url(booking_url)

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
                html_file = f"booking_{origin}_{destination}_{departure_date}.html"
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
        Parse flight data from Frontier booking page HTML.

        Note: The user mentioned needing to click a "gowild" box.
        This might mean GoWild flights are in a separate section or
        require JavaScript interaction.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        flights = []

        logger.info("📄 Parsing booking page HTML...")

        # Check page title
        title = soup.find('title')
        logger.info(f"Page title: {title.text if title else 'None'}")

        # Look for GoWild-specific elements
        gowild_elements = soup.find_all(text=lambda t: t and 'gowild' in str(t).lower())
        logger.info(f"Found {len(gowild_elements)} 'GoWild' mentions")

        # Strategy 1: Look for flight containers
        # Common patterns on booking pages
        flight_selectors = [
            'div[class*="flight"]',
            'div[class*="fare"]',
            'div[class*="option"]',
            'div[data-test*="flight"]',
            'article',
            '.flight-card',
            '.fare-option',
        ]

        all_flight_containers = []
        for selector in flight_selectors:
            containers = soup.select(selector)
            if containers:
                logger.info(f"  Found {len(containers)} elements with selector: {selector}")
                all_flight_containers.extend(containers)

        # Strategy 2: Look for time elements (flights always have times)
        time_elements = soup.find_all('time')
        logger.info(f"Found {len(time_elements)} time elements")

        # Strategy 3: Look for price elements
        price_elements = soup.find_all(text=lambda t: t and '$' in str(t))
        logger.info(f"Found {len(price_elements)} price elements")
        if price_elements:
            # Show sample prices
            sample_prices = [p.strip() for p in price_elements[:10] if p.strip()]
            logger.info(f"Sample prices: {sample_prices[:5]}")

        # Strategy 4: Look for duration/stops indicators
        duration_keywords = ['hrs', 'min', 'nonstop', 'stop']
        duration_elements = soup.find_all(text=lambda t: t and any(
            kw in str(t).lower() for kw in duration_keywords
        ))
        logger.info(f"Found {len(duration_elements)} duration/stop indicators")

        # Strategy 5: Look for JSON data
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'flight' in script.string.lower():
                if '{' in script.string:
                    logger.info("Found potential flight JSON in script tag")
                    # Try to extract JSON
                    try:
                        # Look for JSON patterns
                        script_text = script.string
                        if 'var flightData' in script_text or 'flights:' in script_text:
                            logger.info("  Contains flight data structure")
                    except:
                        pass

        # Try to parse based on known test case structure
        # Test case: ORD->CUN on 11/8/25 should show:
        # 1. 7:25 AM ORD -> 12:18 PM CUN (3 hrs 53 min, Nonstop, $80)
        # 2. 10:35 AM ATL -> 1:19 PM CUN (6 hrs 19 min, 1 Stop ATL, $85)

        # Parse flight containers
        for container in all_flight_containers[:20]:  # Limit for initial parsing
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

                # Try to find times
                times = container.find_all('time')
                if not times:
                    # Look for time-like text patterns (e.g., "7:25 AM")
                    time_texts = container.find_all(text=lambda t: t and ':' in str(t) and any(
                        indicator in str(t).upper() for indicator in ['AM', 'PM']
                    ))
                    if len(time_texts) >= 2:
                        flight_data['departure_time'] = time_texts[0].strip()
                        flight_data['arrival_time'] = time_texts[1].strip()
                elif len(times) >= 2:
                    flight_data['departure_time'] = times[0].text.strip()
                    flight_data['arrival_time'] = times[1].text.strip()

                # Try to find prices
                price_texts = container.find_all(text=lambda t: t and '$' in str(t))
                for price_text in price_texts:
                    try:
                        # Extract number from text like "$80" or "$80.00"
                        price_str = price_text.strip().replace('$', '').replace(',', '').split()[0]
                        price = float(price_str)

                        # Heuristic: GoWild prices are typically $0.99-$5
                        # But test case shows $80-$85, so maybe these are regular prices?
                        # Need to see actual HTML to determine
                        if not flight_data['regular_price'] or price < flight_data['regular_price']:
                            if price < 100:  # Reasonable flight price
                                flight_data['regular_price'] = price
                    except:
                        pass

                # Try to find duration
                duration_text = container.find(text=lambda t: t and 'hrs' in str(t).lower() and 'min' in str(t).lower())
                if duration_text:
                    flight_data['duration'] = duration_text.strip()

                # Try to find stops
                stop_text = container.find(text=lambda t: t and 'stop' in str(t).lower())
                if stop_text:
                    if 'nonstop' in stop_text.lower():
                        flight_data['stops'] = 0
                    else:
                        # Try to extract number (e.g., "1 Stop")
                        import re
                        match = re.search(r'(\d+)\s*stop', stop_text.lower())
                        if match:
                            flight_data['stops'] = int(match.group(1))

                # Only add if we found meaningful data
                if flight_data['departure_time'] and flight_data['arrival_time']:
                    flights.append(flight_data)
                    logger.info(f"  Parsed flight: {flight_data['departure_time']} -> {flight_data['arrival_time']}")

            except Exception as e:
                logger.warning(f"Error parsing container: {e}")
                continue

        # If no flights found, do detailed analysis
        if not flights:
            logger.warning("⚠️  No flights parsed - performing detailed HTML analysis")
            self._detailed_html_analysis(soup)

        return flights

    def _detailed_html_analysis(self, soup: BeautifulSoup):
        """Detailed HTML structure analysis for debugging."""
        logger.info("\n" + "="*80)
        logger.info("DETAILED HTML STRUCTURE ANALYSIS")
        logger.info("="*80)

        # Look for specific test case data
        test_times = ['7:25', '12:18', '10:35', '1:19']
        test_prices = ['$80', '$85']

        logger.info("\n🔍 Looking for test case data (ORD->CUN 11/8/25):")
        logger.info("  Expected times: 7:25 AM, 12:18 PM, 10:35 AM, 1:19 PM")
        logger.info("  Expected prices: $80, $85")

        for test_time in test_times:
            time_found = soup.find_all(text=lambda t: t and test_time in str(t))
            if time_found:
                logger.info(f"  ✅ Found '{test_time}': {len(time_found)} occurrences")
            else:
                logger.info(f"  ❌ '{test_time}' not found")

        for test_price in test_prices:
            price_found = soup.find_all(text=lambda t: t and test_price in str(t))
            if price_found:
                logger.info(f"  ✅ Found '{test_price}': {len(price_found)} occurrences")
            else:
                logger.info(f"  ❌ '{test_price}' not found")

        # Analyze structure
        logger.info("\n📊 Page Structure:")

        # Check for common booking page elements
        elements_to_check = [
            ('form', 'Forms'),
            ('button', 'Buttons'),
            ('input', 'Inputs'),
            ('select', 'Selects'),
            ('[class*="gowild"]', 'GoWild classes'),
            ('[id*="gowild"]', 'GoWild IDs'),
        ]

        for selector, label in elements_to_check:
            found = soup.select(selector)
            logger.info(f"  {label}: {len(found)}")

        # Check for JavaScript that might need interaction
        scripts = soup.find_all('script', src=True)
        logger.info(f"\n  External scripts: {len(scripts)}")

        inline_scripts = soup.find_all('script', src=False)
        logger.info(f"  Inline scripts: {len(inline_scripts)}")

        logger.info("\n" + "="*80 + "\n")


async def test_known_route():
    """Test with the known ORD->CUN route on 11/8/25."""
    logger.info("\n" + "="*80)
    logger.info("TESTING WITH KNOWN ROUTE")
    logger.info("="*80)
    logger.info("\nTest Case: ORD -> CUN on 11/8/2025")
    logger.info("Expected Results:")
    logger.info("  Flight 1: 7:25 AM ORD -> 12:18 PM CUN (3h 53m, Nonstop, $80)")
    logger.info("  Flight 2: 10:35 AM ATL -> 1:19 PM CUN (6h 19m, 1 Stop, $85)")
    logger.info("="*80 + "\n")

    scraper = FrontierBookingScraper()

    # Test with known data
    flights = await scraper.search_flights('ORD', 'CUN', '2025-11-08')

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
    else:
        logger.warning("\n⚠️  No flights parsed!")
        logger.warning("Check the saved HTML file: booking_ORD_CUN_2025-11-08.html")
        logger.warning("Look for the structure and update selectors accordingly")

    logger.info("\n" + "="*80)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_known_route())
