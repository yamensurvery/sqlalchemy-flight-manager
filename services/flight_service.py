from datetime import datetime, timezone

from database import SessionLocal
from models import Flight


def upsert_flight(flight_data: dict):
    session = SessionLocal()

    try:
        flight = session.get(Flight, flight_data["flight_id"])
        if flight:
            for key, value in flight_data.items():
                setattr(flight, key, value)
        else:
            flight = Flight(**flight_data)
            session.add(flight)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def update_flight_fields(flight_id: str, **kwargs):
    session = SessionLocal()
    try:
        flight = session.get(Flight, flight_id)
        if not flight:
            raise ValueError(f"Flight {flight_id} not found")
        for key, value in kwargs.items():
            setattr(flight, key, value)
        session.commit()
    except Exception as e:
        session.close()
        raise e
    finally:
        session.close()

def get_flight(flight_id: str):
    session = SessionLocal()
    try:
        return session.get(Flight, flight_id)
    finally:
        session.close()

def get_upcoming_flights_by_route(origin: str, destination: str):
    session = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        return session.query(Flight).filter(
            Flight.origin == origin,
            Flight.destination == destination,
            Flight.departure_time >= now
        ).all()
    finally:
        session.close()
    