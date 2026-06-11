from flask import Blueprint, jsonify, request, current_app, redirect, url_for
from backend.db_connection import get_db
from backend.utils import error_response
from mysql.connector import Error

#the blueprint handles routes for farmer predictions storage
preds_routes=Blueprint("preds_routes", __name__)

#get all data from table
@preds_routes.route("/pastpreds", methods=["GET"])
def get_preds():
    '''
    Return all past predictions from db
    '''
    current_app.logger.info('GET /pred/pastpreds')
    try:
        #select all values and show in db
        query="""SELECT
                    sp.pred_id,
                    sp.farmer_id,
                    sp.type_of_crop,
                    sp.sown,
                    sp.harvested,
                    sp.water_source,
                    sp.predicted_crop,
                    sp.created_at
                FROM saved_crop_preds sp
                LEFT JOIN users u
                    ON u.user_id=sp.farmer_id
                ORDER BY sp.created_at DESC
        """
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(query)
            predslist = cursor.fetchall()

        current_app.logger.info(f'Retrieved {len(predslist)} predictions')
        return jsonify(predslist),200
    except Error as e:
        current_app.logger.error(f'Database error in get_preds: {e}')
        return error_response(str(e))
    
# input prediction when user presses save
@preds_routes.route("/pred", methods=["POST"])
def save_pred():
    current_app.logger.info('POST /pred/pred')
    data = request.get_json()

    required = ["farmer_id", "type_of_crop", "sown",
                "harvested", "water_source"]
    missing = [f for f in required if f not in data]
    if missing:
        return error_response(f"Missing required fields: {missing}", 400)

    # accept either a single crop ("predicted_crop") or a list ("predicted_crops")
    crops = data.get("predicted_crops")
    if crops is None:
        single = data.get("predicted_crop")
        crops = [single] if single is not None else []
    if not isinstance(crops, list):
        crops = [crops]
    if not crops:
        return error_response("Missing required fields: ['predicted_crop(s)']", 400)

    try:
        conn = get_db()
        cur = conn.cursor()
        # one row per recommended crop
        rows = [
            (
                data["farmer_id"],
                data["type_of_crop"],
                data["sown"],
                data["harvested"],
                data["water_source"],
                crop,
            )
            for crop in crops
        ]
        cur.executemany("""
            INSERT INTO saved_crop_preds
                (farmer_id, type_of_crop, sown, harvested,
                 water_source, predicted_crop)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, rows)
        conn.commit()
        saved = cur.rowcount
        cur.close()
        return jsonify({"message": "Prediction saved", "saved": saved}), 201
    except Error as e:
        current_app.logger.error(f"DB error: {e}")
        return error_response("Failed to save prediction", 500)