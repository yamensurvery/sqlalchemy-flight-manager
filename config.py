import os
from dotenv import load_dotenv



load_dotenv() 

class Config:
    AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    UPDATE_INTERVAL_MINUTES = int(os.getenv("UPDATE_INTERVAL_MINUTES", 5))
    DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost/flightsdb")
    

