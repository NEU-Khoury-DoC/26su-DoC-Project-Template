from flask import Blueprint, jsonify, current_app
from mysql.connector import Error

from backend.db_connection import get_db
from backend.utils import error_response

posts_bp = Blueprint("posts_bp", __name__)

@posts_bp.route("/", methods=["GET"])
def list_all_posts():
    current_app.logger.info(f"GET /posts")
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM posts;")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows), 200

@posts_bp.route("/<int:id>", methods=["GET"])
def list_certain_post(id):
    current_app.logger.info(f"GET /posts")
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM posts WHERE post_id = %s;", (id,))
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows), 200

@posts_bp.route("/<int:id>", methods=["DELETE"])
def delete_post(id):
    current_app.logger.info(f'DELETE /posts/')
    try:
        conn = get_db()
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT post_id FROM posts WHERE post_id = %s", (id,))
            if not cursor.fetchone():
                return error_response("Post not found", 404)

            cursor.execute("DELETE FROM posts WHERE post_id = %s", (id,))

        conn.commit()
        current_app.logger.info(f'Deleted post id={id}')
        return jsonify({"message": "Post deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_post: {e}')
        return error_response(str(e))