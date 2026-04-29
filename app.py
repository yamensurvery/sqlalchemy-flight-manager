import logging
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, request
from auth import require_role
from config import Config
from database import init_db
from ingestion.updater import run_update
from validators import validate_patch_fields, validate_status
from services.flight_service import (
    get_flight,
    get_upcoming_flights_by_route,
    update_flight_fields
)
from services.status_service import (
    get_flights_by_status,
    get_delayed_flights,
    get_flights_departing_soon,
    update_flight_status
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/flights/<flight_id>", methods=["GET"])
@require_role("read")
def flight_by_id(flight_id):
    flight = get_flight(flight_id)
    if not flight:
        return jsonify({"error": "Flight not found"}), 404
    return jsonify(flight.to_dict())

@app.route("/flights", methods=["GET"])
@require_role("read")
def flights_by_route():
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    if not origin or not destination:
        return jsonify({"error": "origin and destination are required"}), 400
    flights = get_upcoming_flights_by_route(origin, destination)
    return jsonify([f.to_dict()for f in flights])

@app.route("/flights/status/<status>", methods=["GET"])
@require_role("read")
def flights_by_status(status):
    flights = get_flights_by_status(status)
    return jsonify([f.to_dict() for f in flights])

@app.route("/flights/delayed", methods=["GET"])
@require_role("read")
def delayed_flights():
    min_delay = request.args.get("min_delay_minutes", 15, type=int)
    flights = get_delayed_flights(min_delay)
    return jsonify([f.to_dict() for f in flights])

@app.route("/flights/departing-soon", methods=["GET"])
@require_role("read")
def departing_soon():
    within = request.args.get("within_minutes", 30, type=int)
    flights = get_flights_departing_soon(within)
    return jsonify([f.to_dict() for f in flights])


@app.route("/flights/<flight_id>/status", methods=["PATCH"])
@require_role("write")
def patch_flight_status(flight_id):
    data = request.get_json()
    if not data or "status" not in data:
        return jsonify({"error": "status field is required", "status": 400}), 400
    error, code = validate_status(data["status"])
    if error:
        return jsonify({"error": error, "status": code}), code
    update_flight_status(flight_id, data["status"])
    return jsonify({"message": f"Flight {flight_id} status updated"})

@app.route("/flights/<flight_id>", methods=["PATCH"])
@require_role("write")
def patch_flight(flight_id):
    data = request.get_json()
    error, code = validate_patch_fields(data)
    if error:
        return jsonify({"error": error, "status": code}), code
    update_flight_fields(flight_id, **data)
    return jsonify({"message": f"Flight {flight_id} updated"})

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": str(e), "status": 400}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e), "status": 404}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": str(e), "status": 405}), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "An unexpected error occurred", "status": 500}), 500





# App factory
def create_app():
    # Step 1 — Bootstrap
    logger.info("Initializing database...")
    init_db()

    # Step 2 — Start background scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_update,
        trigger="interval",
        minutes=Config.UPDATE_INTERVAL_MINUTES,
        max_instances=1
    )
    scheduler.start()
    logger.info("Scheduler started.")

    return app

if __name__ == "__main__":
    application = create_app()
    # Step 3 — Start API (blocks main thread)
    application.run(
        host=Config.HOST,
        port=Config.PORT
    )