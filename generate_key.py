from database import init_db, SessionLocal
from models import ApiKey

def generate_key(owner: str, role: str):
    init_db()
    session = SessionLocal()

    try:
        api_key = ApiKey(owner=owner, role=role)
        session.add(api_key)
        session.commit()
        print(f"API Key generated successfully:")
        print(f"  Owner: {api_key.owner}")
        print(f"  Role:  {api_key.role}")
        print(f"  Key:   {api_key.key}")
        print(f"  ID:    {api_key.id}")
    except Exception as e:
        session.rollback()
        print(f"Failed to generate key: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    generate_key(owner="aviationstack", role="read")
    generate_key(owner="admin", role="admin")