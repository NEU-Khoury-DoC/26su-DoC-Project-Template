from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db

users_bp = Blueprint("users_bp", __name__)

@users_bp.route("/<role>", methods=["GET"])
def list_users(role):
    current_app.logger.info(f"GET /user/{role}")
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT user_id, user_name FROM users WHERE user_type = %s;", (role,))
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows), 200

@users_bp.route("/", methods=["POST"])
def create_user():
    payload = request.get_json()
    name = payload.get("user_name")
    utype = payload.get("user_type")
    if not name or not utype:
        return jsonify({"error":"missing fields"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (user_name, user_type, created_by) VALUES (%s,%s,%s)",
        (name, utype, "api_seed"))
    conn.commit()
    cur.close()
    return jsonify({"user_id": cur.lastrowid}), 201