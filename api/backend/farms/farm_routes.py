from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from backend.utils import error_response
from mysql.connector import Error

farms_bp = Blueprint("farms", __name__)


# Get all farms filtered by counttry
@farms_bp.route("/farms", methods=["GET"])
def get_all_farms():
    current_app.logger.info('GET /farms/farms')
    try:
        country = request.args.get("country")
        query = """
            SELECT f.farm_id,
                   f.farm_name,
                   f.user_id,
                   u.user_name AS owner_name,
                   fl.country,
                   fl.latitude,
                   fl.longitude,
                   f.created_at
            FROM farms f
            LEFT JOIN users u ON f.user_id = u.user_id
            LEFT JOIN farms_location fl ON f.farm_id = fl.farm_id
            WHERE 1=1
        """
        params = []

        if country:
            query += " AND fl.country = %s"
            params.append(country)

        query += " ORDER BY f.farm_name"

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            farm_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(farm_list)} farms')
        return jsonify(farm_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_farms: {e}')
        return error_response(str(e))


# Get a single farm by id owner and location dets.
@farms_bp.route("/farms/<int:farm_id>", methods=["GET"])
def get_farm(farm_id):
    current_app.logger.info(f'GET /farms/farms/{farm_id}')
    try:
        query = """
            SELECT f.farm_id,
                   f.farm_name,
                   f.user_id,
                   u.user_name AS owner_name,
                   fl.country,
                   fl.latitude,
                   fl.longitude,
                   f.created_at
            FROM farms f
            LEFT JOIN users u ON f.user_id = u.user_id
            LEFT JOIN farms_location fl ON f.farm_id = fl.farm_id
            WHERE f.farm_id = %s
        """
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, (farm_id,))
            farm = cursor.fetchone()

            if not farm:
                return error_response("Farm not found", 404)

        return jsonify(farm), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_farm: {e}')
        return error_response(str(e))

@farms_bp.route("/farms", methods=["POST"])
def create_farm():
    current_app.logger.info('POST /farms/farms')
    data = request.get_json()

    # farm fields
    required_farm = ["farm_name", "user_id", "created_by"]
    # location fields — required because a farm without a location
    # won't appear on the map or join correctly
    required_loc  = ["longitude", "latitude", "country"]

    missing = [f for f in required_farm + required_loc if f not in data]
    if missing:
        return error_response(f"Missing required fields: {missing}", 400)

    try:
        conn = get_db()
        cur = conn.cursor()

        # 1. Insert farm
        cur.execute("""
            INSERT INTO farms (farm_name, user_id, created_by)
            VALUES (%s, %s, %s)
        """, (data["farm_name"], data["user_id"], data["created_by"]))
        farm_id = cur.lastrowid

        # 2. Insert location using the new farm_id
        cur.execute("""
            INSERT INTO farms_location (farm_id, longitude, latitude, country, created_by)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            farm_id,
            data["longitude"],
            data["latitude"],
            data["country"],
            data["created_by"],
        ))

        conn.commit()
        cur.close()
        return jsonify({"message": "Farm created", "farm_id": farm_id}), 201
    except Error as e:
        conn.rollback()   # if location insert fails, don't leave an orphan farm row
        current_app.logger.error(f"DB error: {e}")
        return error_response("Failed to create farm", 500)


# PUT: update a farm's name
@farms_bp.route("/farms/<int:farm_id>", methods=["PUT"])
def update_farm(farm_id):
    current_app.logger.info(f'PUT /farms/farms/{farm_id}')
    data = request.get_json()

    if "farm_name" not in data:
        return error_response("Missing required field: farm_name", 400)
    if "updated_by" not in data:
        return error_response("Missing required field: updated_by", 400)

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE farms
            SET farm_name = %s, updated_by = %s
            WHERE farm_id = %s
        """, (data["farm_name"], data["updated_by"], farm_id))
        conn.commit()
        cur.close()
        if cur.rowcount == 0:
            return error_response("Farm not found", 404)
        return jsonify({"message": "Farm updated"}), 200
    except Error as e:
        current_app.logger.error(f"DB error: {e}")
        return error_response("Failed to update farm", 500)


# DELETE: remove a farm and its location
# Order matters: delete farms_location first (FK constraint)
@farms_bp.route("/farms/<int:farm_id>", methods=["DELETE"])
def delete_farm(farm_id):
    current_app.logger.info(f'DELETE /farms/farms/{farm_id}')
    try:
        conn = get_db()
        cur = conn.cursor()

        # 1. Delete location first — FK references farms
        cur.execute("DELETE FROM farms_location WHERE farm_id = %s", (farm_id,))
        # 2. Then delete the farm itself
        cur.execute("DELETE FROM farms WHERE farm_id = %s", (farm_id,))

        conn.commit()
        cur.close()
        if cur.rowcount == 0:
            return error_response("Farm not found", 404)
        return jsonify({"message": "Farm and location deleted"}), 200
    except Error as e:
        conn.rollback()
        current_app.logger.error(f"DB error: {e}")
        return error_response("Failed to delete farm", 500)
