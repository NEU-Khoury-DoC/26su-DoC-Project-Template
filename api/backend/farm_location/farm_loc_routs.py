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