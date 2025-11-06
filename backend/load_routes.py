"""Load all Frontier routes into the database."""
import json
from database import SessionLocal, Route, init_db

def load_routes_from_json():
    """Load routes from frontier_routes.json into database."""

    # Initialize database
    init_db()

    # Load routes from JSON
    with open('frontier_routes.json', 'r') as f:
        routes_data = json.load(f)

    print(f"Loading {len(routes_data)} routes...")

    db = SessionLocal()

    try:
        # Clear existing routes
        db.query(Route).delete()

        # Add all routes
        added = 0
        for route_data in routes_data:
            route = Route(
                origin_code=route_data['origin_code'],
                origin_name=route_data['origin_name'],
                destination_code=route_data['destination_code'],
                destination_name=route_data['destination_name'],
                route_code=route_data['route_code'],
                route_display=route_data['route_display'],
            )
            db.add(route)
            added += 1

        db.commit()
        print(f"✅ Added {added} routes to database")

        # Show some stats
        total = db.query(Route).count()
        origins = db.query(Route.origin_code).distinct().count()
        destinations = db.query(Route.destination_code).distinct().count()

        print(f"\n📊 Database Stats:")
        print(f"  Total routes: {total}")
        print(f"  Origin airports: {origins}")
        print(f"  Destination airports: {destinations}")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    load_routes_from_json()
