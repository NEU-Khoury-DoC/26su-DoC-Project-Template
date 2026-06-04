from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request, current_app

from backend.db_connection import get_db
from backend.routes.storage_service import (
    CODE_TO_NAME,
    STRESS_THRESHOLD,
    country_name,
    fetch_daily_history,
    fetch_latest_daily,
    fetch_daily_on_or_before,
    fetch_latest_winter,
    fetch_winters,
    latest_winter_per_country,
    normalize_country_code,
    predict_risk,
    serialize_winter,
    winter_summary,
)
from backend.utils import error_response
from mysql.connector import Error

storage_bp = Blueprint("storage", __name__)


# Daily gas storage history for charts
# Example: GET /stats/storage/history?country=DE
@storage_bp.route("/stats/storage/history", methods=["GET"])
def get_storage_history():
    current_app.logger.info("GET /stats/storage/history")
    country = request.args.get("country")

    if not country:
        return error_response("Missing required query parameter: country", 400)

    code = normalize_country_code(country)
    if code not in CODE_TO_NAME:
        return error_response(f"Unsupported country code: {country}", 400)

    try:
        with get_db().cursor(dictionary=True) as cursor:
            rows = fetch_daily_history(cursor, code)

        if not rows:
            return error_response(
                "No storage history found for this country. Run scripts/seed_gas_storage.py.",
                404,
            )

        history = [
            {
                "date": row["gas_day"].isoformat(),
                "full": round(float(row["full_pct"]), 2),
            }
            for row in rows
        ]

        return jsonify(
            {
                "country": code,
                "country_name": CODE_TO_NAME[code],
                "history": history,
            }
        ), 200
    except Error as e:
        current_app.logger.error("Database error in get_storage_history: %s", e)
        return error_response(str(e))


# Winter feature rows for ML charts and slider defaults
# Example: GET /stats/storage/winters?country=DE
@storage_bp.route("/stats/storage/winters", methods=["GET"])
def get_storage_winters():
    current_app.logger.info("GET /stats/storage/winters")
    country = request.args.get("country")

    try:
        with get_db().cursor(dictionary=True) as cursor:
            if country:
                code = normalize_country_code(country)
                if code not in CODE_TO_NAME:
                    return error_response(f"Unsupported country code: {country}", 400)
                rows = fetch_winters(cursor, code)
            else:
                rows = fetch_winters(cursor)

        if not rows:
            return error_response(
                "No winter data found. Run scripts/seed_gas_storage.py.",
                404,
            )

        return jsonify({"winters": [serialize_winter(row) for row in rows]}), 200
    except Error as e:
        current_app.logger.error("Database error in get_storage_winters: %s", e)
        return error_response(str(e))


# Latest storage headline metrics for Country Snapshot
# Example: GET /countries/DE/storage/summary
@storage_bp.route("/countries/<country_code>/storage/summary", methods=["GET"])
def get_storage_summary(country_code):
    current_app.logger.info("GET /countries/%s/storage/summary", country_code)
    code = normalize_country_code(country_code)

    if code not in CODE_TO_NAME:
        return error_response(f"Unsupported country code: {country_code}", 400)

    try:
        with get_db().cursor(dictionary=True) as cursor:
            latest = fetch_latest_daily(cursor, code)
            if not latest:
                return error_response(
                    "No storage history found for this country. Run scripts/seed_gas_storage.py.",
                    404,
                )

            month_ago_day = latest["gas_day"] - timedelta(days=30)
            month_ago = fetch_daily_on_or_before(cursor, code, month_ago_day)
            delta_30d = None
            if month_ago:
                delta_30d = round(
                    float(latest["full_pct"]) - float(month_ago["full_pct"]), 2
                )

            summary = winter_summary(cursor, code) or {}

        return jsonify(
            {
                "country": code,
                "country_name": CODE_TO_NAME[code],
                "latest_full": round(float(latest["full_pct"]), 2),
                "latest_date": latest["gas_day"].isoformat(),
                "delta_30d": delta_30d,
                "stressed_winters": summary.get("stressed_winters", 0),
                "total_winters": summary.get("total_winters", 0),
                "worst_winter_min": summary.get("worst_winter_min"),
                "worst_winter_year": summary.get("worst_winter_year"),
                "stress_threshold": STRESS_THRESHOLD,
            }
        ), 200
    except Error as e:
        current_app.logger.error("Database error in get_storage_summary: %s", e)
        return error_response(str(e))


# Gas storage risk ranking for Country Comparison
# Example: GET /stats/storage/risk/compare
@storage_bp.route("/stats/storage/risk/compare", methods=["GET"])
def compare_storage_risk():
    current_app.logger.info("GET /stats/storage/risk/compare")
    try:
        with get_db().cursor(dictionary=True) as cursor:
            latest_rows = latest_winter_per_country(cursor)

        if not latest_rows:
            return error_response(
                "No winter data found. Run scripts/seed_gas_storage.py.",
                404,
            )

        countries = []
        for row in latest_rows:
            prediction = predict_risk(
                float(row["storage_at_start"]),
                float(row["storage_trend_30d"]),
                float(row["storage_volatility"]),
            )
            countries.append(
                {
                    **serialize_winter(row),
                    **prediction,
                    "verdict": (
                        "At risk" if prediction["risk_prob"] >= 0.5 else "Not at risk"
                    ),
                }
            )

        countries.sort(key=lambda item: item["risk_prob"], reverse=True)
        return jsonify({"countries": countries}), 200
    except Error as e:
        current_app.logger.error("Database error in compare_storage_risk: %s", e)
        return error_response(str(e))
    except FileNotFoundError:
        return error_response("Gas storage model file is not available on the API server", 503)
    except Exception as e:
        current_app.logger.error("Error in compare_storage_risk: %s", e)
        return error_response(str(e))


# What-if gas storage risk prediction for Gas Storage Risk page
# Example: POST /stats/storage/risk
@storage_bp.route("/stats/storage/risk", methods=["POST"])
def post_storage_risk():
    current_app.logger.info("POST /stats/storage/risk")
    data = request.get_json() or {}

    if "storage_at_start" not in data:
        return error_response("Missing required field: storage_at_start", 400)

    try:
        storage_at_start = float(data["storage_at_start"])
        storage_trend_30d = data.get("storage_trend_30d")
        storage_volatility = data.get("storage_volatility")

        if storage_trend_30d is None or storage_volatility is None:
            country = data.get("country")
            winter = data.get("winter")
            if not country or winter is None:
                return error_response(
                    "Provide storage_trend_30d and storage_volatility, "
                    "or country and winter to look them up from the database.",
                    400,
                )

            code = normalize_country_code(country)
            with get_db().cursor(dictionary=True) as cursor:
                rows = fetch_winters(cursor, code)
            winter_row = next(
                (row for row in rows if int(row["winter_year"]) == int(winter)),
                None,
            )
            if not winter_row:
                return error_response(
                    f"No winter {winter} found for country {code}", 404
                )

            if storage_trend_30d is None:
                storage_trend_30d = winter_row["storage_trend_30d"]
            if storage_volatility is None:
                storage_volatility = winter_row["storage_volatility"]

        prediction = predict_risk(
            storage_at_start,
            float(storage_trend_30d),
            float(storage_volatility),
        )
        return jsonify(
            {
                **prediction,
                "stress_threshold": STRESS_THRESHOLD,
                "country": data.get("country"),
                "winter": data.get("winter"),
            }
        ), 200
    except FileNotFoundError:
        return error_response("Gas storage model file is not available on the API server", 503)
    except (TypeError, ValueError) as e:
        return error_response(f"Invalid input: {e}", 400)
    except Exception as e:
        current_app.logger.error("Error in post_storage_risk: %s", e)
        return error_response(str(e))
