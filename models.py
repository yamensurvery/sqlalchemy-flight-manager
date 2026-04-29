from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.orm import declarative_base
import secrets
from datetime import datetime, timezone


Base = declarative_base()

class Flight(Base):
    __tablename__= "flights"

    flight_id = Column(String(10), primary_key=True)
    airline = Column(String(50))
    origin = Column(String(10))
    destination = Column(String(10))
    status = Column(String(20))
    gate = Column(String(10))
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    actual_departure = Column(DateTime)
    actual_arrival = Column(DateTime)
    delay_minutes = Column(Integer)

    def to_dict(self):
        return {
            "flight_id": self.flight_id,
            "airline": self.airline,
            "origin": self.origin,
            "destination": self.destination,
            "status": self.status,
            "gate": self.gate,
            "departure_time": str(self.departure_time),
            "arrival_time": str(self.arrival_time),
            "actual_departure": str(self.actual_departure) if self.actual_departure else None,
            "actual_arrival": str(self.actual_arrival) if self.actual_arrival else None,
            "delay_minutes": self.delay_minutes
        }
    

class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(String(36), primary_key=True, default=lambda: secrets.token_hex(16))
    key = Column(String(64), unique=True, nullable=False, default=lambda: secrets.token_hex(32))
    owner = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="read")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    