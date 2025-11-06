"""
Frontier GoWild Flight Scraper using browser cookies.

This approach uses cookies from your logged-in browser session to bypass bot detection.
Frontier will see requests as coming from your authenticated session.
"""
import json
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from playwright.async_api import async_playwright, Browser, Page
from bs4 import BeautifulSoup
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CookieBasedScraper:
    """Scraper that uses browser cookies for authentication."""

    def __init__(self, cookies_file: str = "cookies.json", headless: bool = True):
        self.cookies_file = cookies_file
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.base_url = "https://www.flyfrontier.com"

    async def start(self):
        """Initialize browser."""
        logger.info("Starting browser...")
        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )

    async def close(self):
        """Close browser."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def load_cookies(self, context):
        """Load cookies from file if they exist."""
        if os.path.exists(self.cookies_file):
            logger.info(f"Loading cookies from {self.cookies_file}")
            with open(self.cookies_file, 'r') as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
            logger.info(f"Loaded {len(cookies)} cookies")
            return True
        else:
            logger.warning(f"Cookie file {self.cookies_file} not found")
            return False

    async def save_cookies(self, context):
        """Save cookies to file."""
        cookies = await context.cookies()
        with open(self.cookies_file, 'w') as f:
            json.dump(cookies, f, indent=2)
        logger.info(f"Saved {len(cookies)} cookies to {self.cookies_file}")

    async def create_context(self):
        """Create browser context with cookies."""
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        )

        # Load cookies if available
        await self.load_cookies(context)

        # Apply stealth scripts
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => false});
            window.chrome = {runtime: {}};
        """)

        return context

    async def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str
    ) -> List[Dict]:
        """
        Search for flights.

        Args:
            origin: Origin airport code
            destination: Destination airport code
            departure_date: Date in YYYY-MM-DD format
        """
        logger.info(f"Searching: {origin} -> {destination} on {departure_date}")

        context = await self.create_context()
        page = await context.new_page()

        try:
            # Build URL
            url = f"{self.base_url}/flight/select"
            url += f"?tripType=OW"
            url += f"&origin={origin}"
            url += f"&destination={destination}"
            url += f"&departureDate={departure_date}"
            url += f"&numAdults=1&numChildren=0"

            logger.info(f"Navigating to: {url}")

            # Navigate to search page
            await page.goto(url, wait_until='networkidle', timeout=60000)

            # Wait a bit for dynamic content
            await asyncio.sleep(3)

            # Save cookies after navigation
            await self.save_cookies(context)

            # Get page content
            content = await page.content()

            # Save for debugging
            with open('frontier_page.html', 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info("Saved page to frontier_page.html")

            # Check if we got blocked
            if 'Access denied' in content or 'captcha' in content.lower():
                logger.error("❌ Bot detection triggered - page requires CAPTCHA or shows access denied")

                # Take screenshot
                await page.screenshot(path='blocked.png')
                logger.info("Saved screenshot to blocked.png")

                return []

            # Parse flights
            flights = await self.parse_flights(content, origin, destination, departure_date)

            return flights

        except Exception as e:
            logger.error(f"Error during search: {e}")
            try:
                await page.screenshot(path='error.png')
            except:
                pass
            return []

        finally:
            await page.close()
            await context.close()

    async def parse_flights(
        self,
        html_content: str,
        origin: str,
        destination: str,
        date: str
    ) -> List[Dict]:
        """Parse flight data from HTML."""
        soup = BeautifulSoup(html_content, 'html.parser')
        flights = []

        logger.info("Parsing flight data...")

        # These selectors need to be updated based on Frontier's actual HTML
        # Here are some common patterns to look for:

        # Pattern 1: Look for data in script tags (many sites embed JSON)
        scripts = soup.find_all('script', type='application/json')
        for script in scripts:
            try:
                data = json.loads(script.string)
                logger.info(f"Found JSON data in script tag")
                # Parse JSON for flight data
                # This depends on Frontier's structure
            except:
                pass

        # Pattern 2: Look for flight cards
        flight_elements = soup.find_all(['div', 'article'], attrs={
            'data-testid': lambda x: x and 'flight' in str(x).lower() if x else False
        })

        logger.info(f"Found {len(flight_elements)} potential flight elements")

        # Pattern 3: Look for specific class patterns
        for element in flight_elements:
            try:
                flight_info = {
                    'flight_number': 'Unknown',
                    'origin': origin,
                    'destination': destination,
                    'departure_date': date,
                    'departure_time': 'Unknown',
                    'arrival_date': date,
                    'arrival_time': 'Unknown',
                    'gowild_price': None,
                    'regular_price': None,
                    'is_gowild_available': False,
                    'duration': None,
                    'stops': 0,
                    'aircraft': None,
                }

                # Extract details (selectors need to be updated)
                # Example patterns:
                # - time_elem = element.find('time')
                # - price_elem = element.find(class_='price')
                # - gowild_elem = element.find(text=lambda t: 'GoWild' in str(t))

                flights.append(flight_info)

            except Exception as e:
                logger.warning(f"Error parsing flight element: {e}")

        # If no flights found, analyze the page structure
        if not flights:
            logger.info("No flights parsed - analyzing page structure...")
            self._analyze_page_structure(soup)

        return flights

    def _analyze_page_structure(self, soup: BeautifulSoup):
        """Analyze page to help identify correct selectors."""
        logger.info("\n📊 Page Structure Analysis:")

        # Title
        title = soup.find('title')
        logger.info(f"  Title: {title.text if title else 'None'}")

        # Look for elements with 'flight' in class or id
        flight_elements = soup.find_all(lambda tag: tag.get('class') and any('flight' in str(c).lower() for c in tag.get('class', [])))
        logger.info(f"  Elements with 'flight' in class: {len(flight_elements)}")

        # Look for prices
        price_texts = soup.find_all(text=lambda t: t and '$' in str(t))
        logger.info(f"  Price elements found: {len(price_texts)}")
        if price_texts:
            logger.info(f"  Sample prices: {[str(p).strip()[:30] for p in price_texts[:3]]}")

        # Look for GoWild mentions
        gowild_mentions = soup.find_all(text=lambda t: t and 'gowild' in str(t).lower())
        logger.info(f"  'GoWild' mentions: {len(gowild_mentions)}")

        # Look for structured data
        json_ld = soup.find_all('script', type='application/ld+json')
        logger.info(f"  JSON-LD scripts: {len(json_ld)}")


async def main():
    """Test the scraper."""
    scraper = CookieBasedScraper(headless=False)  # Set False to see browser

    try:
        await scraper.start()

        # Test search
        from datetime import timedelta
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

        flights = await scraper.search_flights('DEN', 'LAX', tomorrow)

        print(f"\n{'='*60}")
        print(f"Found {len(flights)} flights")
        for flight in flights:
            print(f"  {flight['origin']} -> {flight['destination']}")
            print(f"  Time: {flight['departure_time']} - {flight['arrival_time']}")
            print(f"  GoWild: ${flight['gowild_price']}" if flight['gowild_price'] else "  GoWild: N/A")
            print()

    finally:
        await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())
