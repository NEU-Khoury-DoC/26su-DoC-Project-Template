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

# --- listing -------------------------------
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
        title = request.args.get("title")
        city_name = request.args.get("city_name")
        university = request.args.get("university")
        price = request.args.get("price")
        property_type = request.args.get("property_type")

        if country:
            query += " AND country.country_name = %s"
            params.append(country)
        if title:
            query += " AND title = %s"
            params.append(title)
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


# --- social indicator types -------------------------------
@housing_bp.route("/social-indicator-types", methods=["GET"])
def get_all_social_indicator_types():
    current_app.logger.info('GET /housing/social-indicator-types')
    try:
        query = "SELECT * FROM social_indicator_types WHERE 1=1"
        params = []

        name = request.args.get("name")
        if name:
            query += " AND name = %s"
            params.append(name)

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            social_indicator_types_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(social_indicator_types_list)} social indicator types')
        return jsonify(social_indicator_types_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_social_indicator_types: {e}')
        return error_response(str(e))


# --- social indicator stats -------------------------------
# @housing_bp.route("/social-indicator-stats", methods=["POST"])
# def get_crime():
#     current_app.logger.info('POST /housing/social-indicator-stats')
#     try:
#         url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_mddw05"
#         response = requests.get(url, params={"format": "JSON", "lang": "EN"})
#         data = response.json()

#         values = data["value"]
#         countries = data["dimension"]["geo"]["category"]["index"]
#         years = data["dimension"]["time"]["category"]["index"]

#         rows = []
#         for country_code, country_idx in countries.items():
#             for year, year_idx in years.items():
#                 key = str(country_idx * len(years) + year_idx)
#                 value = values.get(key)
#                 if value is not None:
#                     rows.append((country_code, year, value))

#         with get_db().cursor() as cursor:
#             cursor.executemany("""
#                 INSERT INTO social_indicator_stats (country_id, sit_id, year, value)
#                 SELECT c.country_id, 2, %s, %s
#                 FROM country c
#                 WHERE c.country_code = %s
#             """, [(year, value, country_code) for country_code, year, value in rows])
#             get_db().commit()

#         return jsonify({"message": f"Synced {len(rows)} records"}), 201
#     except Exception as e:
#         current_app.logger.error(f'Error syncing Eurostat data: {e}')
#         return error_response(str(e))

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



def sync_eurostat(url, sit_id):
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
                rows.append((sit_id, year, value, country_code))

    with get_db().cursor() as cursor:
        cursor.executemany("""
            INSERT INTO social_indicator_stats (country_id, sit_id, year, value)
            SELECT c.country_id, %s, %s, %s
            FROM country c
            WHERE c.country_code = %s
        """, rows)
        get_db().commit()

    return len(rows)

def get_stats_by_sit_id(sit_id):
    country = request.args.get("country")
    year = request.args.get("year")

    query = """
        SELECT sis.stats_id, c.country_name, c.country_code, sis.year, sis.value
        FROM social_indicator_stats sis
        JOIN country c ON sis.country_id = c.country_id
        WHERE sis.sit_id = %s
    """
    params = [sit_id]

    if country:
        query += " AND c.country_name = %s"
        params.append(country)
    if year:
        query += " AND sis.year = %s"
        params.append(year)

    with get_db().cursor(dictionary=True) as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()
    

# --- Pollution (sit_id = 1) -------------------------------
@housing_bp.route("/social-indicator-stats/pollution", methods=["POST"])
def sync_pollution():
    current_app.logger.info('POST /housing/social-indicator-stats/pollution')
    try:
        count = sync_eurostat(
            "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_mddw05",
            sit_id=1
        )
        return jsonify({"message": f"Synced {count} pollution records"}), 201
    except Exception as e:
        current_app.logger.error(f'Error syncing pollution data: {e}')
        return error_response(str(e))


@housing_bp.route("/social-indicator-stats/pollution", methods=["GET"])
def get_pollution_stats():
    current_app.logger.info('GET /housing/social-indicator-stats/pollution')
    try:
        return jsonify(get_stats_by_sit_id(1)), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_pollution_stats: {e}')
        return error_response(str(e))

# --- Crime (sit_id = 2) -------------------------------

@housing_bp.route("/social-indicator-stats/crime", methods=["POST"])
def sync_crime():
    current_app.logger.info('POST /housing/social-indicator-stats/crime')
    try:
        count = sync_eurostat(
            "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_mddw03",
            sit_id=2
        )
        return jsonify({"message": f"Synced {count} crime records"}), 201
    except Exception as e:
        current_app.logger.error(f'Error syncing crime data: {e}')
        return error_response(str(e))


@housing_bp.route("/social-indicator-stats/crime", methods=["GET"])
def get_crime_stats():
    current_app.logger.info('GET /housing/social-indicator-stats/crime')
    try:
        return jsonify(get_stats_by_sit_id(2)), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_crime_stats: {e}')
        return error_response(str(e))


# --- Poverty (sit_id = 3) -------------------------------

@housing_bp.route("/social-indicator-stats/poverty", methods=["POST"])
def sync_poverty():
    current_app.logger.info('POST /housing/social-indicator-stats/poverty')
    try:
        count = sync_eurostat(
            "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_lvho07a",
            sit_id=3
        )
        return jsonify({"message": f"Synced {count} poverty records"}), 201
    except Exception as e:
        current_app.logger.error(f'Error syncing poverty data: {e}')
        return error_response(str(e))


@housing_bp.route("/social-indicator-stats/poverty", methods=["GET"])
def get_poverty_stats():
    current_app.logger.info('GET /housing/social-indicator-stats/poverty')
    try:
        return jsonify(get_stats_by_sit_id(3)), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_poverty_stats: {e}')
        return error_response(str(e))


# --- Overcrowding (sit_id = 4) -----------------------------
@housing_bp.route("/social-indicator-stats/overcrowding", methods=["POST"])
def sync_overcrowding():
    current_app.logger.info('POST /housing/social-indicator-stats/overcrowding')
    try:
        count = sync_eurostat(
            "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_lvho07b",
            sit_id=4
        )
        return jsonify({"message": f"Synced {count} overcrowding records"}), 201
    except Exception as e:
        current_app.logger.error(f'Error syncing overcrowding data: {e}')
        return error_response(str(e))
    

@housing_bp.route("/social-indicator-stats/overcrowding", methods=["GET"])
def get_overcrowding_stats():
    current_app.logger.info('GET /housing/social-indicator-stats/overcrowding')
    try:
        return jsonify(get_stats_by_sit_id(4)), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_overcrowding_stats: {e}')
        return error_response(str(e))

# --- Noise (sit_id = 5) -------------------------------

@housing_bp.route("/social-indicator-stats/noise", methods=["POST"])
def sync_noise():
    current_app.logger.info('POST /housing/social-indicator-stats/noise')
    try:
        count = sync_eurostat(
            "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_mddw04__custom_21476822",
            sit_id=5
        )
        return jsonify({"message": f"Synced {count} noise records"}), 201
    except Exception as e:
        current_app.logger.error(f'Error syncing noise data: {e}')
        return error_response(str(e))


@housing_bp.route("/social-indicator-stats/noise", methods=["GET"])
def get_noise_stats():
    current_app.logger.info('GET /housing/social-indicator-stats/noise')
    try:
        return jsonify(get_stats_by_sit_id(5)), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_noise_stats: {e}')
        return error_response(str(e))

# --- House Price Index (sit_id = 6) -------------------------------

@housing_bp.route("/social-indicator-stats/hpi", methods=["POST"])
def sync_hpi():
    current_app.logger.info('POST /housing/social-indicator-stats/hpi')
    try:
        count = sync_eurostat(
            "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hpi_inw",
            sit_id=6
        )
        return jsonify({"message": f"Synced {count} HPI records"}), 201
    except Exception as e:
        current_app.logger.error(f'Error syncing HPI data: {e}')
        return error_response(str(e))


@housing_bp.route("/social-indicator-stats/hpi", methods=["GET"])
def get_hpi_stats():
    current_app.logger.info('GET /housing/social-indicator-stats/hpi')
    try:
        return jsonify(get_stats_by_sit_id(6)), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_hpi_stats: {e}')
        return error_response(str(e))
    

# # Update an existing NGO's information
# # Can update any field except NGO_ID
# # Example: PUT /ngo/ngos/1 with JSON body containing fields to update
# @ngo_bp.route("/ngos/<int:ngo_id>", methods=["PUT"])
# def update_ngo(ngo_id):
#     current_app.logger.info(f'PUT /ngo/ngos/{ngo_id}')
#     try:
#         data = request.get_json()

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

# Reviews routes
# Read review
@housing_bp.route("/reviews", methods=["GET"])
def get_reviews():
    current_app.logger.info('GET /housing/reviews')
    try:
        query = "SELECT * FROM reviews WHERE 1=1 "
        params = []
        
        listing_id = request.args.get("listing_id")
        rating = request.args.get("rating")
        if listing_id:
            query += " AND listing_id = %s"
            params.append(listing_id)
        if rating:
            query += " AND rating = %s"
            params.append(rating)

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            reviews_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(reviews_list)} reviews')
        return jsonify(reviews_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_reviews: {e}')
        return error_response(str(e))
    
#Create a new review
@housing_bp.route("/reviews", methods=["POST"])
def create_review():
    current_app.logger.info('POST /housing/reviews')
    try:
        data = request.get_json()

        required_fields = ["listing_id", "rating", "comment"]
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}", 400)

        query = """
            INSERT INTO Reviews (listing_id, rating, comment)
            VALUES (%s, %s, %s)
        """
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, (
                data["listing_id"],
                data.get("rating"),
                data["comment"]
            ))
            new_id = cursor.lastrowid

        get_db().commit()
        current_app.logger.info(f'Created review with id={new_id}')
        return jsonify({"message": "Review created successfully", "review_id": new_id}), 201
    except Error as e:
        current_app.logger.error(f'Database error in create_review: {e}')
        return error_response(str(e))


# Update an existing listing's information
# Can update any field except review_id
# Example: PUT /housing/review/1 with JSON body containing fields to update
@housing_bp.route("/review/<int:review_id>", methods=["PUT"])
def update_review(review_id):
    current_app.logger.info(f'PUT /housing/review/{review_id}')
    try:
        data = request.get_json()

        # Build update query dynamically based on provided fields
        allowed_fields = ["rating", "comment"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return error_response("No valid fields to update", 400)

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT review_id FROM reviews WHERE review_id = %s", (review_id))
            if not cursor.fetchone():
                return error_response("Review not found", 404)

            params.append(review_id)
            query = f"UPDATE reviews SET {', '.join(update_fields)} WHERE review_id = %s"
            cursor.execute(query, params)

        get_db().commit()
        return jsonify({"message": "Review updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_review: {e}')
        return error_response(str(e))

# Delete a review
# Example: DELETE /housing/review/1
@housing_bp.route("/review/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    current_app.logger.info(f'DELETE /housing/review/{review_id}')
    try:
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT review_id FROM reviews WHERE review_id = %s", (review_id))
            if not cursor.fetchone():
                return error_response("Review not found", 404)

            cursor.execute("DELETE FROM reviews WHERE review_id = %s", (review_id))

        get_db().commit()
        current_app.logger.info(f'Deleted review id={review_id}')
        return jsonify({"message": "Review deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_review: {e}')
        return error_response(str(e))



# Funding routes
# Read Funding
@housing_bp.route("/funding", methods=["GET"])
def get_funding():
    current_app.logger.info('GET /housing/funding')
    try:
        query = "SELECT * FROM funding JOIN country ON funding.country_id = country.country_id WHERE 1=1 "
        params = []
        
        country = request.args.get("country")
        year = request.args.get("year")
        amount = request.args.get("amount")
        program = request.args.get("program")
        agency = request.args.get("agency")
        
        if country:
            query += " AND country.country_name = %s"
            params.append(country)
        if year:
            query += " AND year = %s"
            params.append(year)
        if amount:
            query += " AND amount = %s"
            params.append(amount)
        if program:
            query += " AND program = %s"
            params.append(program)
        if agency:
            query += " AND agency = %s"
            params.append(agency)

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            funding_list = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(funding_list)} funding records')
        return jsonify(funding_list), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_funding: {e}')
        return error_response(str(e))

#Create a new funding record
@housing_bp.route("/funding", methods=["POST"])
def create_funding():
    current_app.logger.info('POST /housing/funding')
    try:
        data = request.get_json()

        required_fields = ["funding_id", "country_id", "amount", "program", "agency"]
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}", 400)

        query = """
            INSERT INTO funding (funding_id, country_id, amount, program, agency)
            VALUES (%s, %s, %s, %s, %s)
        """
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query, (
                data["funding_id"],
                data["country_id"],
                data["amount"],
                data["program"],
                data["agency"]
            ))
            new_id = cursor.lastrowid

        get_db().commit()
        current_app.logger.info(f'Created funding record with id={new_id}')
        return jsonify({"message": "Funding plan created successfully", "funding_id": new_id}), 201
    except Error as e:
        current_app.logger.error(f'Database error in create_funding: {e}')
        return error_response(str(e))


# Update an existing funding record
# Can update any field except funding_id
# Example: PUT /housing/funding/1 with JSON body containing fields to update
@housing_bp.route("/housing/funding/<int:funding_id>", methods=["PUT"])
def update_funding(funding_id):
    current_app.logger.info(f'PUT /housing/funding/{funding_id}')
    try:
        data = request.get_json()

        # Build update query dynamically based on provided fields
        allowed_fields = ["amount", "program", "agency"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return error_response("No valid fields to update", 400)

        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT funding_id FROM funding WHERE funding_id = %s", (funding_id))
            if not cursor.fetchone():
                return error_response("Funding record not found", 404)

            params.append(funding_id)
            query = f"UPDATE funding SET {', '.join(update_fields)} WHERE funding_id = %s"
            cursor.execute(query, params)

        get_db().commit()
        return jsonify({"message": "Funding record updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_funding: {e}')
        return error_response(str(e))

# Delete a funding record
# Example: DELETE /housing/funding/1
@housing_bp.route("/housing/funding/<int:funding_id>", methods=["DELETE"])
def delete_funding(funding_id):
    current_app.logger.info(f'DELETE /housing/funding/{funding_id}')
    try:
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT funding_id FROM funding WHERE funding_id = %s", (funding_id))
            if not cursor.fetchone():
                return error_response("Funding record not found", 404)

            cursor.execute("DELETE FROM funding WHERE funding_id = %s", (funding_id,))

        get_db().commit()
        current_app.logger.info(f'Deleted funding id={funding_id}')
        return jsonify({"message": "Funding record deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_funding: {e}')
        return error_response(str(e))
