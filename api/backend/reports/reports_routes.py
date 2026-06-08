from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db

reports_bp = Blueprint("reports_bp", __name__)

@reports_bp.route('/', methods=['POST'])
def create_report():
    current_app.logger.info("POST /reports/")
    data = request.get_json() or {}

    title = data.get('title')
    texts = data.get('texts')
    created_by = data.get('created_by', 'unknown')

    if not title or not texts:
        return jsonify({"error": "missing title or texts"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO saved_reports (title, texts, created_by) VALUES (%s, %s, %s)',
        (title, texts, created_by)
    )
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    return jsonify({"saved_report_id": new_id}), 201

@reports_bp.route('/', methods=['GET'])
def get_reports():
    current_app.logger.info("GET /reports/")
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM saved_reports ORDER BY created_at DESC')
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows), 200