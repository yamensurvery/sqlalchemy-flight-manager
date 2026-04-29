from datetime import datetime, timezone, timedelta

from database import SessionLocal
from models import Flight


def get_flights_by_status(status: str):
    session = SessionLocal()
    try:
        return session.query(Flight).filter(
            Flight.status == status
        ).all()
    finally:
        session.close()


def update_flight_status(flight_id: str, new_status: str):
    session = SessionLocal()
    try:
        flight = session.get(Flight, flight_id)
        if not flight:
            raise ValueError(f"Flight {flight_id} not found")
        flight.status = new_status
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_delayed_flights(min_delay_minutes: int = 15):
    session = SessionLocal()
    try:
        return session.query(Flight).filter(
            Flight.delay_minutes >= min_delay_minutes
        ).all()
    finally:
        session.close()
    
def get_flights_departing_soon(within_minutes: int = 30):
    session = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        window = now + timedelta(minutes = within_minutes)
        return session.query(Flight).filter(
            Flight.departure_time >= now,
            Flight.departure_time <= window
        ).all()
    finally:
        session.close()