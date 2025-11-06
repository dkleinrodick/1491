"""
Frontier GoWild Flight Scraper using Scrapfly.io

This scraper uses Scrapfly for JavaScript rendering and bot detection bypass,
then parses the HTML using BeautifulSoup.
"""
import logging
from typing import List, Dict, Optional
from datetime import datetime
from scrapfly import ScrapflyClient, ScrapeConfig
from bs4 import BeautifulSoup

from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScrapflyFrontierScraper:
    """
    Scraper for Frontier Airlines GoWild flights using Scrapfly.io

    Scrapfly provides:
    - Automatic bot detection bypass
    - JavaScript rendering
    - Built-in extraction with templates
    - No need for manual HTML parsing
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Scrapfly scraper.

        Args:
            api_key: Scrapfly API key (defaults to settings.scrapfly_api_key)
        """
        self.api_key = api_key or settings.scrapfly_api_key
        self.scrapfly = ScrapflyClient(key=self.api_key)
        self.base_url = "https://booking.flyfrontier.com/Flight/InternalSelect"

        # Extraction template for flight data
        # This tells Scrapfly exactly what to extract and where to find it
        self.flight_template = {
            "flights": {
                "selector": ".ibe-flight-info",
                "multiple": True,
                "fields": {
                    "departure_time": {
                        "selector": ".ibe-flight-time-depart .ibe-flight-select-time:first",
                        "type": "text"
                    },
                    "departure_airport": {
                        "selector": ".ibe-flight-time-depart .depart-station-name:first",
                        "type": "text"
                    },
                    "arrival_time": {
                        "selector": ".ibe-flight-time-arrive .ibe-flight-select-time:last",
                        "type": "text"
                    },
                    "arrival_airport": {
                        "selector": ".ibe-flight-time-arrive .arrival-station-name:last",
                        "type": "text"
                    },
                    "duration": {
                        "selector": ".ibe-flight-duration-time strong",
                        "type": "text"
                    },
                    "stops": {
                        "selector": ".ibe-flight-duration-stops",
                        "type": "text"
                    },
                    "price": {
                        "selector": ".ibe-farebox-fare-basic .ibe-flightselect-flight-special-fare",
                        "type": "text"
                    },
                    "actual_fare": {
                        "selector": ".ibe-farebox-fare-basic input.js-fare",
                        "type": "attribute",
                        "attribute": "gowildfare"
                    }
                }
            }
        }

        logger.info("✅ ScrapflyFrontierScraper initialized")

    def build_url(self, origin: str, destination: str, date_str: str, passengers: int = 1) -> str:
        """
        Build Frontier booking URL for GoWild flights.

        Args:
            origin: Origin airport code (e.g., "ORD")
            destination: Destination airport code (e.g., "CUN")
            date_str: Date in YYYY-MM-DD format
            passengers: Number of adult passengers (default: 1)

        Returns:
            Complete booking URL
        """
        # Parse date to get the correct format
        # Frontier seems to accept YYYY-MM-DD format in the URL
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            frontier_date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            logger.warning(f"Invalid date format: {date_str}, using as-is")
            frontier_date = date_str

        # Build URL with GoWild flight type (ftype=GW)
        url = f"{self.base_url}?"
        url += f"o1={origin.upper()}"
        url += f"&d1={destination.upper()}"
        url += f"&dd1={frontier_date}"
        url += f"&adt={passengers}"
        url += "&ftype=GW"  # GoWild flights!

        logger.info(f"Built URL: {url}")
        return url

    async def search_flights(
        self,
        origin: str,
        destination: str,
        date: str,
        passengers: int = 1,
        save_html: bool = True
    ) -> List[Dict]:
        """
        Search for GoWild flights on a specific route and date.

        Args:
            origin: Origin airport code
            destination: Destination airport code
            date: Date in YYYY-MM-DD format
            passengers: Number of passengers
            save_html: Whether to save the HTML response

        Returns:
            List of flight dictionaries with parsed data
        """
        url = self.build_url(origin, destination, date, passengers)

        logger.info(f"🔍 Scraping: {origin} → {destination} on {date}")

        try:
            # Scrape with Scrapfly
            result = self.scrapfly.scrape(
                ScrapeConfig(
                    url=url,
                    render_js=True,  # Enable JavaScript rendering
                    wait_for_selector='.ibe-flight-info'  # Wait for flights to load
                )
            )

            # Save HTML if requested
            if save_html:
                filename = f"frontier_{origin}_{destination}_{date}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result.content)
                logger.info(f"💾 Saved HTML to {filename}")

            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(result.content, 'html.parser')

            # Find all flight elements
            flight_elements = soup.select('.ibe-flight-info')

            if not flight_elements:
                logger.warning("⚠️  No flights found in HTML")
                return []

            logger.info(f"✅ Found {len(flight_elements)} flight elements")

            # Parse each flight
            processed_flights = []
            for flight_elem in flight_elements:
                processed_flight = self._parse_flight_element(
                    flight_elem, origin, destination, date
                )
                if processed_flight:
                    processed_flights.append(processed_flight)

            logger.info(f"✅ Processed {len(processed_flights)} flights successfully")
            return processed_flights

        except Exception as e:
            logger.error(f"❌ Error scraping flights: {e}")
            raise

    def _parse_flight_element(
        self,
        flight_elem,
        origin: str,
        destination: str,
        date: str
    ) -> Optional[Dict]:
        """
        Parse a flight element using BeautifulSoup selectors.

        Args:
            flight_elem: BeautifulSoup element for a single flight
            origin: Origin airport code
            destination: Destination airport code
            date: Departure date

        Returns:
            Normalized flight dictionary for database storage
        """
        try:
            # Extract departure time
            departure_time_elem = flight_elem.select_one('.ibe-flight-time-depart .ibe-flight-select-time')
            departure_time = departure_time_elem.get_text(strip=True) if departure_time_elem else ''

            # Extract arrival time
            arrival_time_elem = flight_elem.select_one('.ibe-flight-time-arrive .ibe-flight-select-time')
            arrival_time = arrival_time_elem.get_text(strip=True) if arrival_time_elem else ''

            # Extract duration
            duration_elem = flight_elem.select_one('.ibe-flight-duration-time strong')
            duration_str = duration_elem.get_text(strip=True) if duration_elem else ''
            duration = self._parse_duration(duration_str)

            # Extract stops
            stops_elem = flight_elem.select_one('.ibe-flight-duration-stops')
            stops_str = stops_elem.get_text(strip=True) if stops_elem else 'Nonstop'
            stops = self._parse_stops(stops_str)

            # Extract price - try the gowildfare attribute first, then the display price
            price = 0.0
            fare_input = flight_elem.select_one('.ibe-farebox-fare-basic input.js-fare')
            if fare_input and fare_input.has_attr('gowildfare'):
                price_str = fare_input['gowildfare']
                price = self._parse_price(price_str)
            else:
                # Fallback to display price
                price_elem = flight_elem.select_one('.ibe-farebox-fare-basic .ibe-flightselect-flight-special-fare')
                if price_elem:
                    price_str = price_elem.get_text(strip=True)
                    price = self._parse_price(price_str)

            # Build normalized flight record
            normalized = {
                'flight_number': f"{origin}{destination}",  # We'll improve this when we find it in HTML
                'origin': origin.upper(),
                'destination': destination.upper(),
                'departure_date': date,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'duration_minutes': duration,
                'stops': stops,
                'gowild_price': price,
                'regular_price': None,  # Not available in GoWild search
                'is_gowild_available': True,
                'scraped_at': datetime.utcnow()
            }

            logger.debug(f"Parsed flight: {departure_time} → {arrival_time} (${price})")
            return normalized

        except Exception as e:
            logger.error(f"Error parsing flight element: {e}")
            return None

    def _parse_price(self, price_str: str) -> float:
        """Parse price string to float."""
        try:
            # Remove $ and any other non-numeric characters except decimal point
            clean_price = ''.join(c for c in str(price_str) if c.isdigit() or c == '.')
            return float(clean_price) if clean_price else 0.0
        except (ValueError, TypeError):
            return 0.0

    def _parse_duration(self, duration_str: str) -> int:
        """
        Parse duration string to minutes.

        Examples:
            "3 hrs 53 min" -> 233
            "1 hr 30 min" -> 90
        """
        try:
            duration_str = duration_str.lower()
            hours = 0
            minutes = 0

            # Extract hours
            if 'hr' in duration_str:
                hrs_part = duration_str.split('hr')[0].strip()
                hours = int(''.join(c for c in hrs_part if c.isdigit()))

            # Extract minutes
            if 'min' in duration_str:
                min_part = duration_str.split('hr')[-1].split('min')[0].strip()
                minutes = int(''.join(c for c in min_part if c.isdigit()))

            return hours * 60 + minutes
        except (ValueError, AttributeError):
            return 0

    def _parse_stops(self, stops_str: str) -> int:
        """
        Parse stops string to integer.

        Examples:
            "Nonstop" -> 0
            "1 Stop" -> 1
            "2 Stops" -> 2
        """
        stops_str = stops_str.lower()
        if 'nonstop' in stops_str or 'non-stop' in stops_str:
            return 0

        # Extract number
        for char in stops_str:
            if char.isdigit():
                return int(char)

        return 0

    def find_cheapest_flight(self, flights: List[Dict]) -> Optional[Dict]:
        """Find the cheapest flight from a list."""
        if not flights:
            return None
        return min(flights, key=lambda f: f.get('gowild_price', float('inf')))

    def find_fastest_flight(self, flights: List[Dict]) -> Optional[Dict]:
        """Find the fastest flight from a list."""
        if not flights:
            return None
        return min(flights, key=lambda f: f.get('duration_minutes', float('inf')))


async def test_scraper():
    """Test the Scrapfly scraper with the known test case."""
    logger.info("=" * 80)
    logger.info("Testing Scrapfly Scraper")
    logger.info("=" * 80)

    # Test case: ORD → CUN on 11/8/2025
    # Expected: 2 flights
    # Flight 1: 7:25 AM ORD → 12:18 PM CUN (3h 53m, Nonstop, $80)
    # Flight 2: 10:35 AM ATL → 1:19 PM CUN (6h 19m, 1 Stop, $85)

    scraper = ScrapflyFrontierScraper()

    logger.info("\n📋 Test Case: ORD → CUN on 2025-11-08")
    logger.info("Expected Results:")
    logger.info("  Flight 1: 7:25 AM → 12:18 PM (3h 53m, Nonstop, $80)")
    logger.info("  Flight 2: 10:35 AM → 1:19 PM (6h 19m, 1 Stop, $85)")
    logger.info("")

    try:
        flights = await scraper.search_flights('ORD', 'CUN', '2025-11-08')

        if not flights:
            logger.error("❌ No flights found!")
            return

        logger.info(f"\n✅ Found {len(flights)} flights:\n")

        for i, flight in enumerate(flights, 1):
            logger.info(f"Flight {i}:")
            logger.info(f"  Times: {flight['departure_time']} → {flight['arrival_time']}")
            logger.info(f"  Duration: {flight['duration_minutes']} minutes")
            logger.info(f"  Stops: {flight['stops']}")
            logger.info(f"  Price: ${flight['gowild_price']}")
            logger.info("")

        # Find best flights
        cheapest = scraper.find_cheapest_flight(flights)
        fastest = scraper.find_fastest_flight(flights)

        if cheapest:
            logger.info(f"💰 Cheapest: ${cheapest['gowild_price']} ({cheapest['departure_time']})")

        if fastest:
            duration_hrs = fastest['duration_minutes'] // 60
            duration_mins = fastest['duration_minutes'] % 60
            logger.info(f"⚡ Fastest: {duration_hrs}h {duration_mins}m ({fastest['departure_time']})")

        # Validation
        logger.info("\n" + "=" * 80)
        logger.info("Validation:")
        logger.info("=" * 80)

        if len(flights) >= 2:
            logger.info("✅ Found at least 2 flights (matches test case)")
        else:
            logger.warning(f"⚠️  Expected 2 flights, found {len(flights)}")

        # Check for expected times
        times = [f['departure_time'] for f in flights]
        if any('7:25' in t for t in times):
            logger.info("✅ Found expected departure time: 7:25 AM")
        else:
            logger.warning("⚠️  Did not find 7:25 AM departure")

        # Check for expected prices
        prices = [f['gowild_price'] for f in flights]
        if any(79 <= p <= 81 for p in prices):
            logger.info("✅ Found expected price: ~$80")
        else:
            logger.warning("⚠️  Did not find ~$80 price")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_scraper())
