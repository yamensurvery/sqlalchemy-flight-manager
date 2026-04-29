from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from models import Base



engine = create_engine(Config.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)