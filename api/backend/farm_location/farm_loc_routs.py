from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from backend.utils import error_response
from mysql.connector import Error

farms_loc_bp = Blueprint("farm_locs", __name__)


# Get all farm locations
@farms_loc_bp.route("/", methods=["GET"])
def get_all_farms():
    current_app.logger.info('GET /farm_loc')
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT farm_id, longitude, latitude, country FROM farms_location")
        rows = cur.fetchall()
        cur.close()
        return jsonify(rows), 200
    except Error as e:
        current_app.logger.error(f"DB error: {e}")
        return error_response("Failed to fetch farms", 500)


# Get specific farm location by farm_id
@farms_loc_bp.route("/<int:farm_id>", methods=["GET"])
def get_farm_by_id(farm_id):
    current_app.logger.info(f'GET /farm_loc/{farm_id}')
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT farm_id, longitude, latitude, country FROM farms_location WHERE farm_id = %s",
            (farm_id,)
        )
        row = cur.fetchone()
        cur.close()
        if row is None:
            return error_response("Farm not found", 404)
        return jsonify(row), 200
    except Error as e:
        current_app.logger.error(f"DB error: {e}")
        return error_response("Failed to fetch farm", 500)
    
@farms_loc_bp.route("/", methods=["POST"])
def create_farm_location():
    current_app.logger.info('POST /farm_loc')
    data = request.get_json()

    required = ["farm_id", "longitude", "latitude", "country", "created_by"]
    missing = [f for f in required if f not in data]
    if missing:
        return error_response(f"Missing required fields: {missing}", 400)

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO farms_location (farm_id, longitude, latitude, country, created_by)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data["farm_id"],
            data["longitude"],
            data["latitude"],
            data["country"],
            data["created_by"],
        ))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        return jsonify({"message": "Farm location created", "farm_data_id": new_id}), 201
    except Error as e:
        current_app.logger.error(f"DB error: {e}")
        return error_response("Failed to create farm location", 500)


# PUT: update a farm's location
@farms_loc_bp.route("/<int:farm_id>", methods=["PUT"])
def update_farm_location(farm_id):
    current_app.logger.info(f'PUT /farm_loc/{farm_id}')
    data = request.get_json()

    updatable = ["longitude", "latitude", "country"]
    updates = {k: v for k, v in data.items() if k in updatable}
    if not updates:
        return error_response("No valid fields to update", 400)
    if "updated_by" not in data:
        return error_response("Missing required field: updated_by", 400)

    updates["updated_by"] = data["updated_by"]
    set_clause = ", ".join(f"{col} = %s" for col in updates)
    params = list(updates.values()) + [farm_id]

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(f"""
            UPDATE farms_location
            SET {set_clause}
            WHERE farm_id = %s
        """, params)
        conn.commit()
        cur.close()
        if cur.rowcount == 0:
            return error_response("Farm location not found", 404)
        return jsonify({"message": "Farm location updated"}), 200
    except Error as e:
        current_app.logger.error(f"DB error: {e}")
        return error_response("Failed to update farm location", 500)


# DELETE: remove a farm location record
@farms_loc_bp.route("/<int:farm_id>", methods=["DELETE"])
def delete_farm_location(farm_id):
    current_app.logger.info(f'DELETE /farm_loc/{farm_id}')
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM farms_location WHERE farm_id = %s",
            (farm_id,)
        )
        conn.commit()
        cur.close()
        if cur.rowcount == 0:
            return error_response("Farm location not found", 404)
        return jsonify({"message": "Farm location deleted"}), 200
    except Error as e:
        current_app.logger.error(f"DB error: {e}")
        return error_response("Failed to delete farm location", 500)