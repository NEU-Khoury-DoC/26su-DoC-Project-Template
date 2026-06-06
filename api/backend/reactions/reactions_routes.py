from flask import Blueprint, jsonify, request, current_app
from mysql.connector import Error

from backend.db_connection import get_db
from backend.utils import error_response

reactions_bp = Blueprint("reactions_bp", __name__)


@reactions_bp.route('/post/<int:post_id>', methods=['GET'])
def list_reactions_for_post(post_id):
    current_app.logger.info(f"GET /reactions/post/{post_id}")
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM reactions WHERE post_id = %s ORDER BY created_at DESC;", (post_id,))
        rows = cur.fetchall()
        cur.close()
        return jsonify(rows), 200
    except Error as e:
        current_app.logger.error(f"Database error in list_reactions_for_post: {e}")
        return error_response(str(e))


@reactions_bp.route('/post/<int:post_id>', methods=['POST'])
def add_reaction_to_post(post_id):
    """Add a new reaction to a post.

    Accepts JSON body: { "pos_neg": true|false } OR { "reaction": "like"|"dislike" }
    Optional: user_id, created_by
    """
    payload = request.get_json(silent=True) or {}
    pos_neg = payload.get('pos_neg')
    reaction = payload.get('reaction')
    user_id = payload.get('user_id')

    if pos_neg is None and reaction is None:
        return error_response('missing reaction (pos_neg or reaction)', 400)

    if pos_neg is None:
        # allow 'like'/'dislike'
        if isinstance(reaction, str) and reaction.lower() in ('like', 'positive', 'pos'):
            pos_neg = True
        else:
            pos_neg = False

    try:
        conn = get_db()
        with conn.cursor() as cur:
            # ensure post exists
            cur.execute("SELECT post_id FROM posts WHERE post_id = %s", (post_id,))
            if not cur.fetchone():
                return error_response('Post not found', 404)

            if user_id is not None:
                cur.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
                if not cur.fetchone():
                    return error_response('User not found', 404)

            created_by = payload.get('created_by', 'api')
            cur.execute(
                "INSERT INTO reactions (pos_neg, post_id, user_id, created_by) VALUES (%s,%s,%s,%s)",
                (pos_neg, post_id, user_id, created_by)
            )

        conn.commit()
        return jsonify({"reaction_id": cur.lastrowid}), 201
    except Error as e:
        current_app.logger.error(f"Database error in add_reaction_to_post: {e}")
        return error_response(str(e))


@reactions_bp.route('/<int:reaction_id>', methods=['PUT'])
def update_reaction(reaction_id):
    payload = request.get_json(silent=True) or {}
    pos_neg = payload.get('pos_neg')
    reaction = payload.get('reaction')
    if pos_neg is None and reaction is None:
        return error_response('missing reaction update (pos_neg or reaction)', 400)

    if pos_neg is None:
        pos_neg = True if str(reaction).lower() in ('like', 'positive', 'pos') else False

    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("SELECT reaction_id FROM reactions WHERE reaction_id = %s", (reaction_id,))
            if not cur.fetchone():
                return error_response('Reaction not found', 404)

            cur.execute("UPDATE reactions SET pos_neg = %s, updated_by = %s WHERE reaction_id = %s", (pos_neg, payload.get('updated_by', 'api'), reaction_id))

        conn.commit()
        return jsonify({"message": "Reaction updated"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in update_reaction: {e}")
        return error_response(str(e))


@reactions_bp.route('/<int:reaction_id>', methods=['DELETE'])
def delete_reaction(reaction_id):
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("SELECT reaction_id FROM reactions WHERE reaction_id = %s", (reaction_id,))
            if not cur.fetchone():
                return error_response('Reaction not found', 404)

            cur.execute("DELETE FROM reactions WHERE reaction_id = %s", (reaction_id,))

        conn.commit()
        return jsonify({"message": "Reaction deleted"}), 200
    except Error as e:
        current_app.logger.error(f"Database error in delete_reaction: {e}")
        return error_response(str(e))
