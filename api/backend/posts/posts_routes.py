from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db

users_bp = Blueprint("posts_bp", __name__)

@users_bp.route("/", methods=["GET"])
def list_all_posts():
    current_app.logger.info(f"GET /posts")
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM posts;")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows), 200

@users_bp.route("/<id>", methods=["GET"])
def list_certain_post(id):
    current_app.logger.info(f"GET /posts")
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(f"SELECT * FROM posts WHERE post_id = {id};")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows), 200
