from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from backend.utils import error_response
from mysql.connector import Error

farms_bp = Blueprint("farms", __name__)


# GET: all farms filtered by country
@farms_bp.route("/country", methods=["GET"])
def get_all_farms():
    current_app.logger.info('GET /farms/country')
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

        with get_db().cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute(query, params)
            farm_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(farm_list)} farms')
        return jsonify(farm_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_farms: {e}')
        return error_response(str(e))


# GET: single farm by farm_id with location details
@farms_bp.route("/farm_id/<int:farm_id>", methods=["GET"])
def get_farm(farm_id):
    current_app.logger.info(f'GET /farms/farm_id/{farm_id}')
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
        with get_db().cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute(query, (farm_id,))
            farm = cursor.fetchone()

            if not farm:
                return error_response("Farm not found", 404)

        return jsonify(farm), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_farm: {e}')
        return error_response(str(e))


# GET: all farms for a user, with locations grouped as a list
@farms_bp.route("/user/<int:user_id>", methods=["GET"])
def get_farm_by_user(user_id):
    current_app.logger.info(f'GET /farms/user/{user_id}')
    try:
        query = """
            SELECT f.farm_id,
                f.farm_name,
                f.user_id,
                u.user_name AS owner_name,
                f.created_at,
                fl.farm_data_id,
                fl.country,
                fl.latitude,
                fl.longitude
            FROM farms f
            LEFT JOIN users u ON f.user_id = u.user_id
            LEFT JOIN farms_location fl ON f.farm_id = fl.farm_id
            WHERE f.user_id = %s
        """
        with get_db().cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

            if not rows:
                return error_response("You do not own any farms!", 404)

            farms_dict = {}
            for row in rows:
                fid = row["farm_id"]
                if fid not in farms_dict:
                    farms_dict[fid] = {
                        "farm_id":    row["farm_id"],
                        "farm_name":  row["farm_name"],
                        "user_id":    row["user_id"],
                        "owner_name": row["owner_name"],
                        "created_at": str(row["created_at"]),
                        "locations":  []
                    }
                if row["farm_data_id"] is not None:
                    farms_dict[fid]["locations"].append({
                        "location_id": row["farm_data_id"],
                        "country":     row["country"],
                        "latitude":    row["latitude"],
                        "longitude":   row["longitude"],
                    })

        return jsonify(list(farms_dict.values())), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_farm_by_user: {e}')
        return error_response(str(e))


# POST: create a farm and its first location atomically
@farms_bp.route("/", methods=["POST"])
def create_farm():
    current_app.logger.info('POST /farms/')
    data = request.get_json()

    required_farm = ["farm_name", "user_id", "created_by"]
    required_loc  = ["longitude", "latitude", "country"]

    missing = [f for f in required_farm + required_loc if f not in data]
    if missing:
        return error_response(f"Missing required fields: {missing}", 400)

    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO farms (farm_name, user_id, created_by)
            VALUES (%s, %s, %s)
        """, (data["farm_name"], data["user_id"], data["created_by"]))
        farm_id = cur.lastrowid

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
        conn.rollback()
        current_app.logger.error(f"DB error: {e}")
        return error_response("Failed to create farm", 500)


# PUT: update a farm's name
@farms_bp.route("/farm_id/<int:farm_id>", methods=["PUT"])
def update_farm(farm_id):
    current_app.logger.info(f'PUT /farms/farm_id/{farm_id}')
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
        if cur.rowcount == 0:
            cur.close()
            return error_response("Farm not found", 404)
        cur.close()
        return jsonify({"message": "Farm updated"}), 200
    except Error as e:
        current_app.logger.error(f"DB error: {e}")
        return error_response("Failed to update farm", 500)


# DELETE: remove a farm (cascade handles locations + growing records)
@farms_bp.route("/farm_id/<int:farm_id>", methods=["DELETE"])
def delete_farm(farm_id):
    current_app.logger.info(f'DELETE /farms/farm_id/{farm_id}')
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM farms WHERE farm_id = %s", (farm_id,))
        conn.commit()
        if cur.rowcount == 0:
            cur.close()
            return error_response("Farm not found", 404)
        cur.close()
        return jsonify({"message": "Farm deleted"}), 200
    except Error as e:
        current_app.logger.error(f"DB error: {e}")
        return error_response("Failed to delete farm", 500)