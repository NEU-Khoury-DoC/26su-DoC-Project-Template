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
