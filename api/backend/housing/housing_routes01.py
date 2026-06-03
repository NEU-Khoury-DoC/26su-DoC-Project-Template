from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from backend.utils import error_response
from mysql.connector import Error
import requests

# Variable name includes the domain (ngo_bp) so it stays readable when
# imported alongside other blueprints (e.g. `from ... import ngo_bp, donor_bp`).
housing_bp = Blueprint("housing", __name__)

# --- country -------------------------------
@housing_bp.route("/country", methods=["GET"])
def get_country():
    current_app.logger.info('GET /housing/country')
    try:
        query = "SELECT * FROM country WHERE 1=1 "
        params = []
        
        country = request.args.get("country")
        if country:
            query += " AND Country = %s"
            params.append(country)

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            country_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(country_list)} countries')
        return jsonify(country_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_countries: {e}')
        return error_response(str(e))

#User routes
@housing_bp.route("/user", methods=["GET"])
def get_user():
    current_app.logger.info('GET /housing/user')
    try:
        query = "SELECT * FROM user JOIN country on user.country_id = country.country_id WHERE 1=1 "
        params = []
        
        name = request.args.get("name")
        country = request.args.get("country")
        role = request.args.get("role")
        if name:
            query += " AND name = %s"
            params.append(name)
        if country:
            query += " AND country.country_name = %s"
            params.append(country)
        if role:
            query += " AND role = %s"
            params.append(role)


        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            user_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(user_list)} users')
        return jsonify(user_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_users: {e}')
        return error_response(str(e))
    
#Update user
@housing_bp.route("/housing/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    current_app.logger.info(f'PUT /housing/user/{user_id}')
    try:
        data = request.get_json()

        #which fields can be updated
        allowed_fields = ["university", "country", "email", "max_budget"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return error_response("No valid fields to update", 400)

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT user_id FROM user WHERE user_id = %s", (user_id))
            if not cursor.fetchone():
                return error_response("User not found", 404)

            params.append(user_id)
            query = f"UPDATE user SET {', '.join(update_fields)} WHERE user_id = %s"
            cursor.execute(query, params)

        get_db().commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_user: {e}')
        return error_response(str(e))
