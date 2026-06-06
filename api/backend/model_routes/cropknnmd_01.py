from flask import Blueprint, jsonify, current_app, redirect, url_for
from backend.simple.playlist import sample_playlist_data

# This blueprint handles basic routes useful for testing and demonstration
crop_routes = Blueprint("crop_routes", __name__)

from backend.ml_models import model01, model02, model03_knn as model03
@crop_routes.route("/model3/prediction/<N>/<P>/<K>/<type_of_crop>/<temperature>/<season>/<sown>/<harvested>/<water_source>/<relative_humidity>", methods=["GET"])
def get_model3_prediction(N, P, K, type_of_crop, temperature, season, sown, harvested, water_source, relative_humidity):
    current_app.logger.info("GET /model3/prediction handler")
    try:
        prediction = model03.predict(
            N=N, P=P, K=K,
            TYPE_OF_CROP=type_of_crop,
            TEMPERATURE=temperature,
            SEASON=season,
            SOWN=sown,
            HARVESTED=harvested,
            WATER_SOURCE=water_source,
            RELATIVE_HUMIDITY=relative_humidity,
        )
        return jsonify({
            "prediction": prediction,
            "input_variables": {
                "N": float(N), "P": float(P), "K": float(K),
                "TYPE_OF_CROP": type_of_crop,
                "TEMPERATURE": float(temperature),
                "SEASON": season,
                "SOWN": sown,
                "HARVESTED": harvested,
                "WATER_SOURCE": water_source,
                "RELATIVE_HUMIDITY": float(relative_humidity),
            },
        }), 200
    except ValueError as e:
        current_app.logger.error(f"model03 input error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"model03 prediction error: {e}")
        return jsonify({"error": "Error processing prediction request"}), 500


@crop_routes.route("/model3/observations", methods=["GET"])
def get_model3_observations():
    current_app.logger.info("GET /model3/observations handler")
    try:
        data = model03.get_observations_with_predictions()
        return jsonify(data), 200
    except Exception as e:
        current_app.logger.error(f"model03 observations error: {e}")
        return jsonify({"error": "Error fetching observations"}), 500