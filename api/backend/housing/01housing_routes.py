from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from backend.utils import error_response
from mysql.connector import Error
import requests

# Variable name includes the domain (ngo_bp) so it stays readable when
# imported alongside other blueprints (e.g. `from ... import ngo_bp, donor_bp`).
housing_bp = Blueprint("housing", __name__)


@housing_bp.route("/country", methods=["READ"])
def get_all_countries():
    current_app.logger.info('READ /housing/country')
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


@housing_bp.route("/listing", methods=["GET"])
def get_all_listings():
    current_app.logger.info('GET /housing/listing')
    try:
        query = "SELECT * FROM listing " \
        "JOIN country ON listing.country_id = country.country_id " \
        "JOIN university ON listing.associated_university_id = university.university_id " \
        "WHERE 1=1"
        params = []

        country = request.args.get("country")
        city_name = request.args.get("city_name")
        university = request.args.get("university")
        price = request.args.get("price")
        property_type = request.args.get("property_type")

        if country:
            query += " AND country.country_name = %s"
            params.append(country)
        if city_name:
            query += " AND city_name = %s"
            params.append(city_name)
        if university:
            query += " AND university.university_name = %s"
            params.append(university)
        if price:
            query += " AND price <= %s"
            params.append(price)
        if property_type:
            query += " AND property_type = %s"
            params.append(property_type)


        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            listing_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(listing_list)} listings')
        return jsonify(listing_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_listings: {e}')
        return error_response(str(e))

@housing_bp.route("/social-indicator-stats", methods=["POST"])
def get_crime():
    current_app.logger.info('POST /housing/social-indicator-stats')
    try:
        url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_mddw05"
        response = requests.get(url, params={"format": "JSON", "lang": "EN"})
        data = response.json()

        values = data["value"]
        countries = data["dimension"]["geo"]["category"]["index"]
        years = data["dimension"]["time"]["category"]["index"]

        rows = []
        for country_code, country_idx in countries.items():
            for year, year_idx in years.items():
                key = str(country_idx * len(years) + year_idx)
                value = values.get(key)
                if value is not None:
                    rows.append((country_code, year, value))

        with get_db().cursor() as cursor:
            cursor.executemany("""
                INSERT INTO social_indicator_stats (country_id, sit_id, year, value)
                SELECT c.country_id, 2, %s, %s
                FROM country c
                WHERE c.country_name = %s
            """, [(year, value, country_code) for country_code, year, value in rows])
            get_db().commit()

        return jsonify({"message": f"Synced {len(rows)} records"}), 201
    except Exception as e:
        current_app.logger.error(f'Error syncing Eurostat data: {e}')
        return error_response(str(e))

@housing_bp.route("/social-indicator-stats", methods=["GET"])
def get_social_indicator_stats():
    current_app.logger.info('GET /housing/social-indicator-stats')
    try:
        country = request.args.get("country")
        year = request.args.get("year")
        type = request.args.get("social_indicator_type")

        query = "SELECT * FROM social_indicator_stats " \
        "JOIN social_indicator_types ON social_indicator_stats.sit_id = social_indicator_types.sit_id " \
        "JOIN country ON social_indicator_stats.country_id = country.country_id " \
        "WHERE 1=1"
        params = []

        if country:
            query += " AND country.country_name = %s"
            params.append(country)
        if year:
            query += " AND year = %s"
            params.append(year)
        if type:
            query += " AND social_indicator_types.name = %s"
            params.append(type)

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            stats = cursor.fetchall()

        return jsonify(stats), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_social_indicator_stats: {e}')
        return error_response(str(e))



@housing_bp.route("/listing", methods=["POST"])
def create_listing():
    current_app.logger.info('POST /housing/listing')
    try:
        data = request.get_json()

        required_fields = ["country_id", "user_id", "price", "property_type", "city_name"]
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}", 400)

        query = """
            INSERT INTO Listings (Country, User, Price, Property_Type, City)
            VALUES (%s, %s, %s, %s, %s)
        """
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, (
                data["country_id"],
                data["user_id"],
                data["price"],
                data["property_type"],
                data["city_name"],
            ))
            new_id = cursor.lastrowid

        get_db().commit()
        current_app.logger.info(f'Created listing with id={new_id}')
        return jsonify({"message": "Listing created successfully", "listing_id": new_id}), 201
    except Error as e:
        current_app.logger.error(f'Database error in create_listing: {e}')
        return error_response(str(e))


# # Update an existing NGO's information
# # Can update any field except NGO_ID
# # Example: PUT /ngo/ngos/1 with JSON body containing fields to update
# @ngo_bp.route("/ngos/<int:ngo_id>", methods=["PUT"])
# def update_ngo(ngo_id):
#     current_app.logger.info(f'PUT /ngo/ngos/{ngo_id}')
#     try:
#         data = request.get_json()

#         # Build update query dynamically based on provided fields
#         allowed_fields = ["Name", "Country", "Founding_Year", "Focus_Area", "Website"]
#         update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
#         params = [data[f] for f in allowed_fields if f in data]

#         if not update_fields:
#             return error_response("No valid fields to update", 400)

#         with get_db().cursor(dictionary=True) as cursor:
#             cursor.execute("SELECT NGO_ID FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
#             if not cursor.fetchone():
#                 return error_response("NGO not found", 404)

#             params.append(ngo_id)
#             query = f"UPDATE WorldNGOs SET {', '.join(update_fields)} WHERE NGO_ID = %s"
#             cursor.execute(query, params)

#         get_db().commit()
#         return jsonify({"message": "NGO updated successfully"}), 200
#     except Error as e:
#         current_app.logger.error(f'Database error in update_ngo: {e}')
#         return error_response(str(e))


# # Delete an NGO
# # Example: DELETE /ngo/ngos/1
# @ngo_bp.route("/ngos/<int:ngo_id>", methods=["DELETE"])
# def delete_ngo(ngo_id):
#     current_app.logger.info(f'DELETE /ngo/ngos/{ngo_id}')
#     try:
#         with get_db().cursor(dictionary=True) as cursor:
#             cursor.execute("SELECT NGO_ID FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))
#             if not cursor.fetchone():
#                 return error_response("NGO not found", 404)

#             cursor.execute("DELETE FROM WorldNGOs WHERE NGO_ID = %s", (ngo_id,))

#         get_db().commit()
#         current_app.logger.info(f'Deleted NGO id={ngo_id}')
#         return jsonify({"message": "NGO deleted successfully"}), 200
#     except Error as e:
#         current_app.logger.error(f'Database error in delete_ngo: {e}')
#         return error_response(str(e))

