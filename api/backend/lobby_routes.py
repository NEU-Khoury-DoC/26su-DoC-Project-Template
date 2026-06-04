from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from backend.utils import error_response
from mysql.connector import Error
from backend.ml_models import lobby_model

organizations_bp = Blueprint("organizations", __name__)
policy_bp        = Blueprint("policy", __name__)
countries_bp     = Blueprint("countries", __name__)
users_bp         = Blueprint("users", __name__)
ml_bp            = Blueprint("ml", __name__)



# Route 1 — GET /organizations
# Search / filter all organizations by policy area, country, or industry.
@organizations_bp.route("/organizations", methods=["GET"])
def get_all_organizations():
    current_app.logger.info("GET /organizations")
    try:
        policy_area = request.args.get("policy_area")
        country     = request.args.get("country")
        industry    = request.args.get("industry")

       
        query  = "SELECT * FROM organization WHERE 1=1"
        params = []

        if policy_area:
            query += """
                AND org_id IN (
                    SELECT org_id FROM lobbying_activity la
                    JOIN policy_area pa ON la.policy_area_id = pa.policy_area_id
                    WHERE pa.name = %s
                )"""
            params.append(policy_area)
        if country:
            query += " AND country_code = %s"
            params.append(country)
        if industry:
            query += """
                AND industry_id IN (
                    SELECT industry_id FROM industry WHERE name = %s
                )"""
            params.append(industry)

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            orgs = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(orgs)} organizations")
        return jsonify(orgs), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_all_organizations: {e}")
        return error_response(str(e))


# Route 2 — GET /organizations/<org_id>
# Full org profile: base info + lobbying activities + expenditures.
@organizations_bp.route("/organizations/<int:org_id>", methods=["GET"])
def get_organization(org_id):
    current_app.logger.info(f"GET /organizations/{org_id}")
    try:
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM organization WHERE org_id = %s", (org_id,))
            org = cursor.fetchone()

            if not org:
                return error_response("Organization not found", 404)

            # Attach lobbying activities
            cursor.execute(
                "SELECT * FROM lobbying_activity WHERE org_id = %s", (org_id,)
            )
            org["lobbying_activities"] = cursor.fetchall()

            # Attach expenditure records
            cursor.execute(
                "SELECT * FROM expenditure_record WHERE org_id = %s", (org_id,)
            )
            org["expenditures"] = cursor.fetchall()

        return jsonify(org), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_organization: {e}")
        return error_response(str(e))


# Route 3 — POST /organizations
# Add a new organization.
# Required fields: name, country_code, industry_id, lobbying_cost
@organizations_bp.route("/organizations", methods=["POST"])
def create_organization():
    current_app.logger.info("POST /organizations")
    try:
        data = request.get_json()

        required_fields = ["name", "country_code", "industry_id", "lobbying_cost"]
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}", 400)

        query = """
            INSERT INTO organization
                (name, lobbyfacts_url, members_eu, members_fte,
                 lobbying_cost, interest_represented, country_code, industry_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, (
                data["name"],
                data.get("lobbyfacts_url"),
                data.get("members_eu"),
                data.get("members_fte"),
                data["lobbying_cost"],
                data.get("interest_represented"),
                data["country_code"],
                data["industry_id"],
            ))
            new_id = cursor.lastrowid

        get_db().commit()
        current_app.logger.info(f"Created organization id={new_id}")
        return jsonify({"message": "Organization created successfully", "org_id": new_id}), 201
    except Error as e:
        current_app.logger.error(f"Database error in create_organization: {e}")
        return error_response(str(e))


# Route 4 — PUT /organizations/<org_id>
# Update any fields on an existing organization.
# Example: PUT /organizations/42 with JSON body containing fields to update
@organizations_bp.route("/organizations/<int:org_id>", methods=["PUT"])
def update_organization(org_id):
    current_app.logger.info(f"PUT /organizations/{org_id}")
    try:
        data = request.get_json()

        allowed_fields = [
            "name", "lobbyfacts_url", "members_eu", "members_fte",
            "lobbying_cost", "interest_represented", "country_code", "industry_id"
        ]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params        = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return error_response("No valid fields to update", 400)

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT org_id FROM organization WHERE org_id = %s", (org_id,))
            if not cursor.fetchone():
                return error_response("Organization not found", 404)

            params.append(org_id)
            query = f"UPDATE organization SET {', '.join(update_fields)} WHERE org_id = %s"
            cursor.execute(query, params)

        get_db().commit()
        return jsonify({"message": "Organization updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in update_organization: {e}")
        return error_response(str(e))


# Route 5 — DELETE /organizations/<org_id>
# Remove an organization from the database.
# Example: DELETE /organizations/42
@organizations_bp.route("/organizations/<int:org_id>", methods=["DELETE"])
def delete_organization(org_id):
    current_app.logger.info(f"DELETE /organizations/{org_id}")
    try:
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT org_id FROM organization WHERE org_id = %s", (org_id,))
            if not cursor.fetchone():
                return error_response("Organization not found", 404)

            cursor.execute("DELETE FROM organization WHERE org_id = %s", (org_id,))

        get_db().commit()
        current_app.logger.info(f"Deleted organization id={org_id}")
        return jsonify({"message": "Organization deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_organization: {e}")
        return error_response(str(e))


# ─────────────────────────────────────────────────────────────────────────────
# BLUEPRINT: policy
# ─────────────────────────────────────────────────────────────────────────────

# Route 6 — GET /policy-areas
# Fetch all policy areas to populate the search dropdown.
# Example: /policy-areas
@policy_bp.route("/policy-areas", methods=["GET"])
def get_policy_areas():
    current_app.logger.info("GET /policy-areas")
    try:
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM policy_area ORDER BY name ASC")
            areas = cursor.fetchall()

        current_app.logger.info(f"Retrieved {len(areas)} policy areas")
        return jsonify(areas), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_policy_areas: {e}")
        return error_response(str(e))


# ─────────────────────────────────────────────────────────────────────────────
# BLUEPRINT: countries
# ─────────────────────────────────────────────────────────────────────────────

# Route 7 — GET /country-indicators/<country_code>
# Fetch GDP, population, and inflation for a given country (Clouseau detail cards).
# Example: /country-indicators/DE
@countries_bp.route("/country-indicators/<string:country_code>", methods=["GET"])
def get_country_indicators(country_code):
    current_app.logger.info(f"GET /country-indicators/{country_code}")
    try:
        with get_db().cursor(dictionary=True) as cursor:
            # Confirm the country exists
            cursor.execute(
                "SELECT * FROM country WHERE country_code = %s", (country_code,)
            )
            country = cursor.fetchone()
            if not country:
                return error_response("Country not found", 404)

            # Get the most recent indicator row for this country
            cursor.execute(
                """SELECT * FROM country_indicator
                   WHERE country_code = %s
                   ORDER BY year DESC""",
                (country_code,)
            )
            country["indicators"] = cursor.fetchall()

        return jsonify(country), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_country_indicators: {e}")
        return error_response(str(e))


# ─────────────────────────────────────────────────────────────────────────────
# BLUEPRINT: users
# ─────────────────────────────────────────────────────────────────────────────

# Route 8 — GET /preferences
# Get the current user's saved policy + country preferences (Stromae feed).
# Example: /preferences?user_id=7
@users_bp.route("/preferences", methods=["GET"])
def get_preferences():
    current_app.logger.info("GET /preferences")
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return error_response("Missing required parameter: user_id", 400)

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT * FROM app_user WHERE user_id = %s", (user_id,)
            )
            user = cursor.fetchone()
            if not user:
                return error_response("User not found", 404)

            # Return saved queries / preferences for this user
            cursor.execute(
                "SELECT * FROM saved_query_export WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,)
            )
            user["saved_queries"] = cursor.fetchall()

        # Don't return password hash to the client
        user.pop("password_hash", None)
        return jsonify(user), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_preferences: {e}")
        return error_response(str(e))


# Route 9 — POST /preferences
# Submit onboarding preferences — policy areas & countries (Stromae onboarding).
# Required fields: user_id, query_json
@users_bp.route("/preferences", methods=["POST"])
def save_preferences():
    current_app.logger.info("POST /preferences")
    try:
        data = request.get_json()

        required_fields = ["user_id", "query_json"]
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}", 400)

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT user_id FROM app_user WHERE user_id = %s", (data["user_id"],)
            )
            if not cursor.fetchone():
                return error_response("User not found", 404)

            cursor.execute(
                """INSERT INTO saved_query_export (user_id, query_json, file_format)
                   VALUES (%s, %s, %s)""",
                (data["user_id"], data["query_json"], data.get("file_format", "json"))
            )
            new_id = cursor.lastrowid

        get_db().commit()
        current_app.logger.info(f"Saved preferences export_id={new_id}")
        return jsonify({"message": "Preferences saved successfully", "export_id": new_id}), 201
    except Error as e:
        current_app.logger.error(f"Database error in save_preferences: {e}")
        return error_response(str(e))


# ─────────────────────────────────────────────────────────────────────────────
# BLUEPRINT: ml
# ─────────────────────────────────────────────────────────────────────────────


# Route 10 — POST /lobby/prediction
# Submit lobbying inputs and return the model prediction.
@ml_bp.route("/lobby/prediction", methods=["POST"])
def get_lobby_prediction():
    current_app.logger.info("POST /lobby/prediction")
    try:
        data = request.get_json(silent=True) or {}

        required_fields = ["lobbying_cost", "ep_passes", "members_fte", "country", "interest"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        prediction = lobby_model.predict(
            data["lobbying_cost"],
            data["ep_passes"],
            data["members_fte"],
            data["country"],
            data["interest"],
        )

        current_app.logger.info(f"lobby prediction returned {prediction:.2f}")
        return jsonify({
            "prediction": round(prediction, 2),
            "input_variables": {
                "lobbying_cost": float(data["lobbying_cost"]),
                "ep_passes": float(data["ep_passes"]),
                "members_fte": float(data["members_fte"]),
                "country": data["country"],
                "interest": data["interest"],
            },
        }), 200

    except ValueError as e:
        current_app.logger.error(f"lobby prediction input error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"lobby prediction error: {e}")
        return jsonify({"error": "Error processing prediction request"}), 500

