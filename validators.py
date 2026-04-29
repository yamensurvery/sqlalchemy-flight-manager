from flask import jsonify

VALID_STATUSES = {"on time", "delayed", "boarding", "landed", "cancelled"}

FLIGHT_FIELDS = {
    "airline": str,
    "origin": str,
    "destination": str,
    "status": str,
    "gate": str,
    "delay_minutes": int
}

def validate_patch_fields(data: dict):
    if not data:
        return "Request body is required", 400
    
    invalid_fields = [k for k in data if k not in FLIGHT_FIELDS]
    if invalid_fields:
        return f"Invalid fields: {', '.join(invalid_fields)}", 400

    for field, value in data.items():
        expected_type = FLIGHT_FIELDS[field]
        if not isinstance(value, expected_type):
            return f"Field '{field}' must be of type {expected_type.__name__}", 400

    if "status" in data and data["status"] not in VALID_STATUSES:
        return f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}", 400

    return None, None

def validate_status(status: str):
    if status not in VALID_STATUSES:
        return f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}", 400
    return None, None