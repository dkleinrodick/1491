"""Add test flight data to the database."""
from database import SessionLocal, Flight
from datetime import datetime, timedelta

# Create database session
db = SessionLocal()

# Sample GoWild flights
test_flights = [
    {
        'flight_number': 'F9-1234',
        'origin': 'DEN',
        'destination': 'LAX',
        'departure_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'departure_time': '08:30',
        'arrival_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'arrival_time': '10:15',
        'gowild_price': 0.99,
        'regular_price': 89.99,
        'is_gowild_available': True,
        'duration': '1h 45m',
        'stops': 0,
        'aircraft': 'A320',
    },
    {
        'flight_number': 'F9-2345',
        'origin': 'DEN',
        'destination': 'LAS',
        'departure_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'departure_time': '12:00',
        'arrival_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'arrival_time': '13:15',
        'gowild_price': 0.99,
        'regular_price': 59.99,
        'is_gowild_available': True,
        'duration': '1h 15m',
        'stops': 0,
        'aircraft': 'A320',
    },
    {
        'flight_number': 'F9-3456',
        'origin': 'DEN',
        'destination': 'PHX',
        'departure_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'departure_time': '14:30',
        'arrival_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'arrival_time': '16:00',
        'gowild_price': 0.99,
        'regular_price': 69.99,
        'is_gowild_available': True,
        'duration': '1h 30m',
        'stops': 0,
        'aircraft': 'A321',
    },
    {
        'flight_number': 'F9-4567',
        'origin': 'LAX',
        'destination': 'MIA',
        'departure_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'departure_time': '09:00',
        'arrival_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'arrival_time': '16:45',
        'gowild_price': 0.99,
        'regular_price': 199.99,
        'is_gowild_available': True,
        'duration': '4h 45m',
        'stops': 0,
        'aircraft': 'A321',
    },
    {
        'flight_number': 'F9-5678',
        'origin': 'MCO',
        'destination': 'DEN',
        'departure_date': datetime.now().strftime('%Y-%m-%d'),
        'departure_time': '15:00',
        'arrival_date': datetime.now().strftime('%Y-%m-%d'),
        'arrival_time': '17:30',
        'gowild_price': 0.99,
        'regular_price': 149.99,
        'is_gowild_available': True,
        'duration': '3h 30m',
        'stops': 0,
        'aircraft': 'A320',
    },
    {
        'flight_number': 'F9-6789',
        'origin': 'DEN',
        'destination': 'SFO',
        'departure_date': datetime.now().strftime('%Y-%m-%d'),
        'departure_time': '18:00',
        'arrival_date': datetime.now().strftime('%Y-%m-%d'),
        'arrival_time': '20:30',
        'gowild_price': 1.99,
        'regular_price': 129.99,
        'is_gowild_available': True,
        'duration': '2h 30m',
        'stops': 0,
        'aircraft': 'A321',
    },
]

# Add flights to database
for flight_data in test_flights:
    flight = Flight(**flight_data)
    db.add(flight)

db.commit()

# Count flights
count = db.query(Flight).count()
gowild_count = db.query(Flight).filter(Flight.is_gowild_available == True).count()

print(f"✅ Added {len(test_flights)} test flights!")
print(f"📊 Total in database: {count} flights")
print(f"✈️  GoWild available: {gowild_count} flights")

db.close()
