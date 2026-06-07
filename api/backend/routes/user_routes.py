from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from backend.utils import error_response
from mysql.connector import Error

VALID_PERSONAS = ("household_owner", "journalist", "energy_trader")

user_bp = Blueprint("users", __name__)


# zeus_api: get_users()
@user_bp.route("/users", methods=["GET"])
def get_users():
    current_app.logger.info("GET /users")
    persona = request.args.get("persona")

    if not persona:
        return error_response("Missing required query parameter: persona", 400)
    if persona not in VALID_PERSONAS:
        return error_response(
            f"Invalid persona. Must be one of: {', '.join(VALID_PERSONAS)}",
            400,
        )

    try:
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(
                """
                SELECT user_id, display_name, persona, first_name
                FROM users
                WHERE persona = %s
                ORDER BY display_name
                """,
                (persona,),
            )
            users = cursor.fetchall()

        current_app.logger.info("Retrieved %s users for persona=%s", len(users), persona)
        return jsonify(users), 200
    except Error as e:
        current_app.logger.error("Database error in get_users: %s", e)
        return error_response(str(e))


# zeus_api: (called directly via requests in Home.py)
@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    current_app.logger.info("GET /users/%s", user_id)
    try:
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(
                """
                SELECT user_id, display_name, persona, first_name
                FROM users
                WHERE user_id = %s
                """,
                (user_id,),
            )
            user = cursor.fetchone()

        if not user:
            return error_response("User not found", 404)

        return jsonify(user), 200
    except Error as e:
        current_app.logger.error("Database error in get_user: %s", e)
        return error_response(str(e))
