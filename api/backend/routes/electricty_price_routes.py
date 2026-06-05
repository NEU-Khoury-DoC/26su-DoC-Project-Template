from flask import Blueprint, jsonify, request
from backend.ml_models.electricity_price_model import predict

electricty_price_bp = Blueprint('electricty_price', __name__)

@electricty_price_bp.route('/forecast', methods=['GET'])
def forecast():
    country_code = request.args.get('country', 'DE').upper()

    valid_countries = ["AT","BE","BG","CZ","DE","ES","FR","HR","HU","LV","NL","PL","PT","RO","SK"]
    if country_code not in valid_countries:
        return jsonify({"error": f"Invalid country code. Must be one of {valid_countries}"}), 400

    try:
        predictions = predict(country_code)
        return jsonify({
            "country": country_code,
            "forecast": predictions
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 404