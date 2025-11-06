"""
FastAPI application for Frontier GoWild Flight Finder.
"""
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from database import get_db, init_db, Flight, Route
from scraper import FrontierScraper
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Frontier GoWild Flight Finder API",
    description="API for searching Frontier Airlines GoWild pass flights",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Frontier GoWild Flight Finder API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/flights", response_model=List[dict])
async def get_flights(
    origin: Optional[str] = Query(None, description="Filter by origin airport code"),
    destination: Optional[str] = Query(None, description="Filter by destination airport code"),
    date: Optional[str] = Query(None, description="Filter by departure date (YYYY-MM-DD)"),
    gowild_only: bool = Query(False, description="Show only GoWild available flights"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get flights from the database with optional filtering.
    """
    query = db.query(Flight)

    # Apply filters
    if origin:
        query = query.filter(Flight.origin == origin.upper())
    if destination:
        query = query.filter(Flight.destination == destination.upper())
    if date:
        query = query.filter(Flight.departure_date == date)
    if gowild_only:
        query = query.filter(Flight.is_gowild_available == True)

    # Order by departure date and time
    query = query.order_by(Flight.departure_date, Flight.departure_time)

    # Limit results
    flights = query.limit(limit).all()

    return [flight.to_dict() for flight in flights]


@app.get("/api/origins", response_model=List[str])
async def get_origins(db: Session = Depends(get_db)):
    """Get all available origin airports."""
    origins = db.query(Flight.origin).distinct().all()
    return sorted([o[0] for o in origins if o[0]])


@app.get("/api/destinations", response_model=List[str])
async def get_destinations(
    origin: Optional[str] = Query(None, description="Filter destinations by origin"),
    db: Session = Depends(get_db)
):
    """Get all available destination airports."""
    query = db.query(Flight.destination).distinct()

    if origin:
        query = query.filter(Flight.origin == origin.upper())

    destinations = query.all()
    return sorted([d[0] for d in destinations if d[0]])


@app.post("/api/scrape/search")
async def trigger_flight_search(
    origin: str = Query(..., description="Origin airport code"),
    destination: str = Query(..., description="Destination airport code"),
    date: str = Query(..., description="Departure date (YYYY-MM-DD)"),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Trigger a flight search for specific route and date.

    This endpoint starts a background task to scrape flight data.
    """
    try:
        # Validate date format
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Check if we have recent data (within last hour)
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    existing = db.query(Flight).filter(
        Flight.origin == origin.upper(),
        Flight.destination == destination.upper(),
        Flight.departure_date == date,
        Flight.scraped_at >= one_hour_ago
    ).first()

    if existing:
        return {
            "status": "cached",
            "message": "Using cached data from less than 1 hour ago",
            "last_updated": existing.scraped_at.isoformat()
        }

    # Add background task to scrape
    if background_tasks:
        background_tasks.add_task(
            scrape_flights_background,
            origin.upper(),
            destination.upper(),
            date,
            db
        )

    return {
        "status": "triggered",
        "message": "Flight search initiated. Check back in a few moments.",
        "origin": origin.upper(),
        "destination": destination.upper(),
        "date": date
    }


@app.post("/api/scrape/bulk")
async def trigger_bulk_scrape(
    origin: str = Query(..., description="Origin airport code"),
    days: int = Query(2, ge=1, le=7, description="Number of days to scrape"),
    background_tasks: BackgroundTasks = None
):
    """
    Trigger a bulk scrape for all destinations from an origin.

    This will search flights for the next N days to all available destinations.
    """
    if background_tasks:
        background_tasks.add_task(
            bulk_scrape_background,
            origin.upper(),
            days
        )

    return {
        "status": "triggered",
        "message": f"Bulk scrape initiated for {origin} for the next {days} days",
        "origin": origin.upper(),
        "days": days,
        "note": "This may take several minutes. Check /api/flights endpoint for results."
    }


async def scrape_flights_background(
    origin: str,
    destination: str,
    date: str,
    db: Session
):
    """Background task to scrape flights."""
    logger.info(f"Starting background scrape: {origin} -> {destination} on {date}")

    try:
        async with FrontierScraper(headless=settings.scraper_headless) as scraper:
            flights = await scraper.search_flights(origin, destination, date)

            # Save to database
            for flight_data in flights:
                flight = Flight(**flight_data)
                db.add(flight)

            db.commit()
            logger.info(f"Successfully scraped {len(flights)} flights")

    except Exception as e:
        logger.error(f"Error in background scrape: {e}")
        db.rollback()


async def bulk_scrape_background(origin: str, days: int):
    """Background task for bulk scraping."""
    logger.info(f"Starting bulk scrape from {origin} for {days} days")

    try:
        async with FrontierScraper(headless=settings.scraper_headless) as scraper:
            # Get all destinations
            destinations = await scraper.get_all_destinations(origin)
            logger.info(f"Found {len(destinations)} destinations from {origin}")

            # Scrape for each day
            for day_offset in range(days):
                date = (datetime.now() + timedelta(days=day_offset)).strftime('%Y-%m-%d')

                for destination in destinations:
                    try:
                        logger.info(f"Scraping {origin} -> {destination} on {date}")
                        flights = await scraper.search_flights(origin, destination, date)

                        # Save to database
                        from database import SessionLocal
                        db = SessionLocal()
                        try:
                            for flight_data in flights:
                                flight = Flight(**flight_data)
                                db.add(flight)
                            db.commit()
                        finally:
                            db.close()

                        # Random delay between requests
                        await scraper.random_delay(3, 7)

                    except Exception as e:
                        logger.error(f"Error scraping {origin}->{destination}: {e}")
                        continue

            logger.info("Bulk scrape completed")

    except Exception as e:
        logger.error(f"Error in bulk scrape: {e}")


@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get database statistics."""
    total_flights = db.query(Flight).count()
    gowild_flights = db.query(Flight).filter(Flight.is_gowild_available == True).count()
    origins = db.query(Flight.origin).distinct().count()
    destinations = db.query(Flight.destination).distinct().count()

    # Get latest scrape time
    latest = db.query(Flight).order_by(Flight.scraped_at.desc()).first()
    last_updated = latest.scraped_at.isoformat() if latest else None

    return {
        "total_flights": total_flights,
        "gowild_available": gowild_flights,
        "origins": origins,
        "destinations": destinations,
        "last_updated": last_updated
    }


@app.get("/api/routes", response_model=List[dict])
async def get_routes(
    origin: Optional[str] = Query(None, description="Filter by origin airport code"),
    destination: Optional[str] = Query(None, description="Filter by destination airport code"),
    search: Optional[str] = Query(None, description="Search in route display names"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get all available Frontier routes.
    """
    query = db.query(Route).filter(Route.is_active == True)

    # Apply filters
    if origin:
        query = query.filter(Route.origin_code == origin.upper())
    if destination:
        query = query.filter(Route.destination_code == destination.upper())
    if search:
        query = query.filter(Route.route_display.contains(search))

    # Order by route code
    query = query.order_by(Route.route_code)

    # Limit results
    routes = query.limit(limit).all()

    return [route.to_dict() for route in routes]


@app.get("/api/routes/origins", response_model=List[dict])
async def get_route_origins(db: Session = Depends(get_db)):
    """Get all unique origin airports with route counts."""
    from sqlalchemy import func

    results = db.query(
        Route.origin_code,
        Route.origin_name,
        func.count(Route.id).label('route_count')
    ).filter(
        Route.is_active == True
    ).group_by(
        Route.origin_code,
        Route.origin_name
    ).order_by(
        Route.origin_code
    ).all()

    return [{
        "code": r.origin_code,
        "name": r.origin_name,
        "route_count": r.route_count
    } for r in results]


@app.post("/api/scrape/single-route")
async def scrape_single_route(
    origin: str = Query(..., description="Origin airport code"),
    destination: str = Query(..., description="Destination airport code"),
    date: str = Query(..., description="Departure date (YYYY-MM-DD)"),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Scrape a single route using Scrapfly.

    This conserves API credits by only scraping one route at a time.
    """
    try:
        # Validate date format
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Find the route
    route = db.query(Route).filter(
        Route.origin_code == origin.upper(),
        Route.destination_code == destination.upper()
    ).first()

    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # Check if recently scraped (within last hour)
    if route.last_scraped:
        from datetime import timedelta
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        if route.last_scraped >= one_hour_ago:
            return {
                "status": "cached",
                "message": "Route was scraped less than 1 hour ago",
                "route": route.to_dict(),
                "last_scraped": route.last_scraped.isoformat()
            }

    # Add background task
    if background_tasks:
        background_tasks.add_task(
            scrape_route_with_scrape_do,
            origin.upper(),
            destination.upper(),
            date,
            route.id,
            db
        )

    return {
        "status": "triggered",
        "message": "Flight search initiated using Scrapfly",
        "route": route.to_dict(),
        "note": "Check /api/flights endpoint in 30-60 seconds for results"
    }


async def scrape_route_with_scrape_do(
    origin: str,
    destination: str,
    date: str,
    route_id: int,
    db: Session
):
    """Background task to scrape a route using Scrapfly."""
    from scrapfly_scraper import ScrapflyFrontierScraper
    from datetime import datetime

    logger.info(f"Background scraping: {origin} -> {destination} on {date}")

    try:
        scraper = ScrapflyFrontierScraper()
        flights = await scraper.search_flights(origin, destination, date)

        # Save flights to database
        for flight_data in flights:
            flight = Flight(**flight_data)
            db.add(flight)

        # Update route scraping metadata
        route = db.query(Route).filter(Route.id == route_id).first()
        if route:
            route.last_scraped = datetime.utcnow()
            route.scrape_count += 1

        db.commit()

        logger.info(f"✅ Scraped {len(flights)} flights for {origin}-{destination}")

    except Exception as e:
        logger.error(f"❌ Error scraping route: {e}")
        db.rollback()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
