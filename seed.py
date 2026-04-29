from datetime import datetime, timezone, timedelta
from database import init_db, SessionLocal
from models import Flight

def seed():
    init_db()
    session = SessionLocal()

    flights = [
        Flight(
            flight_id="DL123",
            airline="Delta",
            origin="ATL",
            destination="JFK",
            status="on time",
            gate="B4",
            departure_time=datetime.now(timezone.utc) + timedelta(hours=2),
            arrival_time=datetime.now(timezone.utc) + timedelta(hours=4),
            actual_departure=None,
            actual_arrival=None,
            delay_minutes=0
        ),
        Flight(
            flight_id="AA456",
            airline="American",
            origin="LAX",
            destination="ORD",
            status="delayed",
            gate="C7",
            departure_time=datetime.now(timezone.utc) + timedelta(hours=1),
            arrival_time=datetime.now(timezone.utc) + timedelta(hours=4),
            actual_departure=None,
            actual_arrival=None,
            delay_minutes=45
        ),
        Flight(
            flight_id="UA789",
            airline="United",
            origin="JFK",
            destination="LAX",
            status="boarding",
            gate="A2",
            departure_time=datetime.now(timezone.utc) + timedelta(minutes=20),
            arrival_time=datetime.now(timezone.utc) + timedelta(hours=6),
            actual_departure=None,
            actual_arrival=None,
            delay_minutes=0
        ),
        Flight(
            flight_id="SW101",
            airline="Southwest",
            origin="ATL",
            destination="JFK",
            status="cancelled",
            gate="D1",
            departure_time=datetime.now(timezone.utc) + timedelta(hours=3),
            arrival_time=datetime.now(timezone.utc) + timedelta(hours=5),
            actual_departure=None,
            actual_arrival=None,
            delay_minutes=0
        ),
    ]

    try:
        session.add_all(flights)
        session.commit()
        print("Seeded database successfully.")
    except Exception as e:
        session.rollback()
        print(f"Seeding failed: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed()