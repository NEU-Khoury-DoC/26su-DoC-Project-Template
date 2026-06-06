from flask import Blueprint, jsonify, current_app, request
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

@posts_bp.route("/", methods=["POST"])
def create_post():
    current_app.logger.info('POST post/')
    try:
        data = request.get_json() or {}

        # expected fields for a post
        required_fields = ["title", "post_text", "user_id"]
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}", 400)

        title = data.get("title")
        post_text = data.get("post_text")
        img = data.get("img")
        user_id = data.get("user_id")
        created_by = data.get("created_by", str(user_id))

        query = (
            "INSERT INTO posts (title, post_text, img, user_id, created_by) "
            "VALUES (%s, %s, %s, %s, %s)"
        )

        conn = get_db()
        cur = conn.cursor()
        cur.execute(query, (title, post_text, img, user_id, created_by))
        new_id = cur.lastrowid
        conn.commit()
        cur.close()

        current_app.logger.info(f'Created post with id={new_id}')
        return jsonify({"message": "Post created successfully", "post_id": new_id}), 201
    except Error as e:
        current_app.logger.error(f'Database error in create_ngo: {e}')
        return error_response(str(e))

@posts_bp.route("/<int:id>", methods=["GET"])
def list_certain_post(id):
    current_app.logger.info(f"GET /posts")
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM posts WHERE post_id = %s;", (id,))
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows), 200


@posts_bp.route("/<int:id>", methods=["PUT"])
def update_post(id):
    current_app.logger.info(f'PUT /posts/{id}')
    try:
        data = request.get_json() or {}

        # allowed fields to update
        allowed_fields = ["title", "post_text", "img", "user_id", "updated_by"]
        update_parts = []
        params = []
        for field in allowed_fields:
            if field in data:
                update_parts.append(f"{field} = %s")
                params.append(data[field])

        if not update_parts:
            return error_response("No fields to update", 400)

        params.append(id)
        query = "UPDATE posts SET " + ", ".join(update_parts) + " WHERE post_id = %s"

        conn = get_db()
        cur = conn.cursor()
        # ensure post exists
        cur.execute("SELECT post_id FROM posts WHERE post_id = %s", (id,))
        if not cur.fetchone():
            cur.close()
            return error_response("Post not found", 404)

        cur.execute(query, tuple(params))
        conn.commit()
        cur.close()

        current_app.logger.info(f'Updated post id={id}')
        return jsonify({"message": "Post updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_post: {e}')
        return error_response(str(e))

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