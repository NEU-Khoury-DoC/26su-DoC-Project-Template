from flask import Blueprint, jsonify, request, current_app
from mysql.connector import Error

from backend.db_connection import get_db
from backend.utils import error_response

comments_bp = Blueprint("comments_bp", __name__)

@comments_bp.route('/post/<int:post_id>', methods=['GET'])
def list_comments_for_post(post_id):
    current_app.logger.info(f"GET /comments/post/{post_id}")
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM comments WHERE post_id = %s ORDER BY created_at DESC;", (post_id,))
        rows = cur.fetchall()
        cur.close()
        return jsonify(rows), 200
    except Error as e:
        current_app.logger.error(f"Database error in list_comments_for_post: {e}")
        return error_response(str(e))


@comments_bp.route('/post/<int:post_id>', methods=['POST'])
def add_comment_to_post(post_id):
    """Add a new comment to a post.

    Expected JSON body: { "text": "...", "user_id": optional }
    If user_id is omitted the comment will be inserted with NULL user_id and
    created_by set to 'anonymous'.
    """
    payload = request.get_json(silent=True) or {}
    text = payload.get('text') or payload.get('texts')
    user_id = payload.get('user_id')

    if not text:
        return error_response('missing comment text', 400)

    try:
        conn = get_db()
        # ensure post exists
        with conn.cursor() as cur:
            cur.execute("SELECT post_id FROM posts WHERE post_id = %s", (post_id,))
            if not cur.fetchone():
                return error_response('Post not found', 404)

            if user_id is not None:
                # verify user exists
                cur.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
                if not cur.fetchone():
                    return error_response('User not found', 404)

            created_by = payload.get('created_by', 'api')
            cur.execute(
                "INSERT INTO comments (texts, post_id, user_id, created_by) VALUES (%s,%s,%s,%s)",
                (text, post_id, user_id, created_by)
            )

        conn.commit()
        return jsonify({"comment_id": cur.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f"Database error in add_comment_to_post: {e}")
        return error_response(str(e))


@comments_bp.route('/user/<int:user_id>', methods=['GET'])
def list_comments_by_user(user_id):
    current_app.logger.info(f"GET /comments/user/{user_id}")
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM comments WHERE user_id = %s ORDER BY created_at DESC;", (user_id,))
        rows = cur.fetchall()
        cur.close()
        return jsonify(rows), 200
    except Error as e:
        current_app.logger.error(f"Database error in list_comments_by_user: {e}")
        return error_response(str(e))


@comments_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    current_app.logger.info(f"GET /comments/{comment_id}")
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM comments WHERE comment_id = %s;", (comment_id,))
        row = cur.fetchone()
        cur.close()
        if not row:
            return error_response('Comment not found', 404)
        return jsonify(row), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_comment: {e}")
        return error_response(str(e))


@comments_bp.route('/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    payload = request.get_json(silent=True) or {}
    text = payload.get('text') or payload.get('texts')
    if not text:
        return error_response('missing comment text', 400)

    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("SELECT comment_id FROM comments WHERE comment_id = %s", (comment_id,))
            if not cur.fetchone():
                return error_response('Comment not found', 404)

            cur.execute("UPDATE comments SET texts = %s, updated_by = %s WHERE comment_id = %s", (text, payload.get('updated_by', 'api'), comment_id))

        conn.commit()
        return jsonify({"message": "Comment updated"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in update_comment: {e}")
        return error_response(str(e))


@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("SELECT comment_id FROM comments WHERE comment_id = %s", (comment_id,))
            if not cur.fetchone():
                return error_response('Comment not found', 404)

            cur.execute("DELETE FROM comments WHERE comment_id = %s", (comment_id,))

        conn.commit()
        return jsonify({"message": "Comment deleted"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_comment: {e}")
        return error_response(str(e))
