from flask import Blueprint, jsonify, current_app, request
from backend.simple.playlist import sample_playlist_data
from backend.ml_models import prices_model
from backend.db_connection import get_db

price_bp = Blueprint("price_bp", __name__)

@price_bp.route("/prediction/<crop>/<country>", methods=["GET"])
def get_model2_prediction(crop, country):
    current_app.logger.info("GET /prices_model/prediction handler")
    try:
        prediction = prices_model.predict(crop, country)
        current_app.logger.info(f"price model prediction: {prediction:.2f}")
        return jsonify({
            "prediction":      round(prediction, 2),
            "input_variables": {
                "Crop": str(crop),
                "Country":     str(country),
            },
        }), 200
    except ValueError as e:
        current_app.logger.error(f"price model input error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"price model prediction error: {e}")
        return jsonify({"error": "Error processing prediction request"}), 500

@price_bp.route('/average', methods=['GET'])
def get_average_prices():
    current_app.logger.info("GET /average")
    year_min = request.args.get('year_min', 2017, type=int)
    year_max = request.args.get('year_max', 2024, type=int)

    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute('''
        SELECT geo, prod_veg, ROUND(AVG(selling_price), 2) as avg_price
        FROM CropPrices
        WHERE year BETWEEN %s AND %s
        GROUP BY geo, prod_veg
    ''', (year_min, year_max))
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows), 200