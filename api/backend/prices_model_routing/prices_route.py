from flask import Blueprint, jsonify, current_app, redirect, url_for
from backend.simple.playlist import sample_playlist_data
from backend.ml_models import prices_model

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

