"""Database configuration and models."""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Flight(Base):
    """Flight model representing a GoWild flight."""

    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)

    # Flight Information
    flight_number = Column(String, nullable=False)
    origin = Column(String, nullable=False, index=True)
    destination = Column(String, nullable=False, index=True)
    departure_date = Column(String, nullable=False, index=True)
    departure_time = Column(String, nullable=False)
    arrival_date = Column(String, nullable=False)
    arrival_time = Column(String, nullable=False)

    # Pricing
    gowild_price = Column(Float, nullable=True)
    regular_price = Column(Float, nullable=True)
    is_gowild_available = Column(Boolean, default=False, index=True)

    # Additional Info
    duration = Column(String, nullable=True)
    stops = Column(Integer, default=0)
    aircraft = Column(String, nullable=True)

    # Metadata
    scraped_at = Column(DateTime, default=datetime.utcnow, index=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "flight_number": self.flight_number,
            "origin": self.origin,
            "destination": self.destination,
            "departure_date": self.departure_date,
            "departure_time": self.departure_time,
            "arrival_date": self.arrival_date,
            "arrival_time": self.arrival_time,
            "gowild_price": self.gowild_price,
            "regular_price": self.regular_price,
            "is_gowild_available": self.is_gowild_available,
            "duration": self.duration,
            "stops": self.stops,
            "aircraft": self.aircraft,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }


def init_db():
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
