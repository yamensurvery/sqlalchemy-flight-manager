from functools import wraps
from flask import request, jsonify
from database import SessionLocal
from models import ApiKey


def require_role(required_role: str):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = request.headers.get("X-API-Key")
            if not key:
                return jsonify({"error": "API key required"}), 401
            
            session = SessionLocal()
            try:
                api_key = session.query(ApiKey).filter(
                    ApiKey.key == key,
                    ApiKey.is_active == True
                ).first()

                if not api_key:
                    return jsonify({"error": "Invalid or inactive API key"}), 401
                
                roles = ["read", "write", "admin"]
                if roles.index(api_key.role) < roles.index(required_role):
                    return jsonify({"error": "Insufficient permissions"}), 403
                
            finally:
                session.close()

            return f(*args, **kwargs)
        return wrapper
    return decorator