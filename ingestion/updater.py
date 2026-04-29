import requests
import logging
from datetime import datetime, timezone

from config import Config
from database import SessionLocal
from services.flight_service import upsert_flight

logger = logging.getLogger(__name__)

AVIATIONSTACK_URL = "http://api.aviationstack.com/v1/flights"

def fetch_flights():

    params = {
        "access_key": Config.AVIATIONSTACK_API_KEY,
        "dep_iata": "LAX",
        "limit": 100
    }
    response = requests.get(AVIATIONSTACK_URL, params=params)
    response.raise_for_status()
    return response.json().get("data", [])

def parse_flight(raw: dict) -> dict:
    departure = raw.get("departure", {})
    arrival = raw.get("arrival", {})

    return {
        "flight_id": raw.get("flight", {}).get("iata"),
        "airline": raw.get("airline", {}).get("name"),
        "origin": departure.get("iata"),
        "destination": arrival.get("iata"),
        "status": raw.get("flight_status"),
        "gate": departure.get("gate"),
        "departure_time": parse_time(departure.get("scheduled")),
        "arrival_time": parse_time(arrival.get("scheduled")),
        "actual_departure": parse_time(departure.get("actual")),
        "actual_arrival": parse_time(arrival.get("actual")),
        "delay_minutes": departure.get("delay") or 0
    }

def parse_time(time_str: str):
    if not time_str:
        return None
    try:
        return datetime.fromisoformat(time_str).astimezone(timezone.utc).replace(tzinfo=None)
    except ValueError:
        return None

def run_update():
    logger.info("Running flight update from AviationStack...")
    try:
        raw_flights = fetch_flights()
        logger.info(f"Fetched {len(raw_flights)} flights from AviationStack.")
        for raw in raw_flights:
            flight_data = parse_flight(raw)
            if not flight_data["flight_id"]:
                continue
            upsert_flight(flight_data)
        logger.info("Flight update complete.")
    except Exception as e:
        logger.error(f"Flight update failed: {e}")
        raise e