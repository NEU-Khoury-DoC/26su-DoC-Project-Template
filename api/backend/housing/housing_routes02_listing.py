from flask import jsonify, request, current_app
from backend.housing.housing_routes01 import housing_bp
from backend.db_connection import get_db
from backend.utils import error_response
from mysql.connector import Error
import requests

# Variable name includes the domain (ngo_bp) so it stays readable when
# imported alongside other blueprints (e.g. `from ... import ngo_bp, donor_bp`).

# --- listing -------------------------------
@housing_bp.route("/listing", methods=["GET"])
def get_listing():
    current_app.logger.info('GET /housing/listing')
    try:
        query = "SELECT * FROM listing " \
        "JOIN country ON listing.country_id = country.country_id " \
        "LEFT JOIN university ON listing.associated_university_id = university.university_id " \
        "WHERE 1=1"
        params = []

        country = request.args.get("country")
        title = request.args.get("title")
        city_name = request.args.get("city_name")
        university = request.args.get("university")
        price = request.args.get("price")
        property_type = request.args.get("property_type")

        if country:
            query += " AND country.country_name = %s"
            params.append(country)
        if title:
            query += " AND listing.title = %s"
            params.append(title)
        if city_name:
            query += " AND listing.city_name = %s"
            params.append(city_name)
        if university:
            query += " AND university.university_name = %s"
            params.append(university)
        if price:
            query += " AND listing.price <= %s"
            params.append(price)
        if property_type:
            query += " AND listing.property_type = %s"
            params.append(property_type)


        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            listing_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(listing_list)} listings')
        return jsonify(listing_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_listings: {e}')
        return error_response(str(e))

#Create a listing
@housing_bp.route("/listing", methods=["POST"])
def create_listing():
    current_app.logger.info('POST /housing/listing')
    try:
        data = request.get_json()

        required_fields = ["country_id", "title", "user_id", "price", "property_type", "city_name"]
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}", 400)

        query = """
            INSERT INTO Listings (country_id, user_id, price, property_type, city_name)
            VALUES (%s, %s, %s, %s, %s)
        """
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, (
                data["country_id"],
                data["title"],
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
@housing_bp.route("/housing/listing/<int:listing_id>", methods=["PUT"])
def update_listing(listing_id):
    current_app.logger.info(f'PUT /housing/listing/{listing_id}')
    try:
        data = request.get_json()

        # Build update query dynamically based on provided fields
        allowed_fields = ["title", "price", "property_type", "city_name"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return error_response("No valid fields to update", 400)

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT listing_id FROM listing WHERE listing_id = %s", (listing_id))
            if not cursor.fetchone():
                return error_response("Listing not found", 404)

            params.append(listing_id)
            query = f"UPDATE listing SET {', '.join(update_fields)} WHERE listing_id = %s"
            cursor.execute(query, params)

        get_db().commit()
        return jsonify({"message": "Listing updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_listing: {e}')
        return error_response(str(e))

# Delete a listing
# Example: DELETE /housing/listing/1
@housing_bp.route("/housing/listing/<int:listing_id>", methods=["DELETE"])
def delete_listing(listing_id):
    current_app.logger.info(f'DELETE /housing/listing/{listing_id}')
    try:
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT listing_id FROM listing WHERE listing_id = %s", (listing_id,))
            if not cursor.fetchone():
                return error_response("Listing not found", 404)

            cursor.execute("DELETE FROM listing WHERE listing_id = %s", (listing_id,))

        get_db().commit()
        current_app.logger.info(f'Deleted listing id={listing_id}')
        return jsonify({"message": "Listing deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_listing: {e}')
        return error_response(str(e))
