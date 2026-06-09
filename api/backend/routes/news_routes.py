import json
import os
import urllib.error
import urllib.parse
import urllib.request

from flask import Blueprint, current_app, jsonify, request

from backend.db_connection import get_db
from backend.news_personalization import (
    build_news_request_strategies,
    filter_and_rank_articles,
    resolve_user_news_filters,
    score_article_relevance,
)
from backend.utils import error_response
from mysql.connector import Error

news_bp = Blueprint("news", __name__)

NEWSDATA_BASE_URL = "https://newsdata.io/api/1/latest"


def _fetch_newsdata(params):
    api_key = os.getenv("NEWSDATA_API_KEY", "").strip()
    if not api_key:
        return None, error_response(
            "NewsData.io API key is not configured. Set NEWSDATA_API_KEY in api/.env.",
            503,
        )

    encoded = urllib.parse.urlencode(params)
    url = f"{NEWSDATA_BASE_URL}?{encoded}"
    current_app.logger.info("NewsData.io request: %s", url.replace(api_key, "***"))

    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            payload = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        current_app.logger.error("NewsData.io HTTP error: %s %s", e.code, body)
        try:
            err = json.loads(body)
            message = err.get("results", {}).get("message") or err.get("message") or body
        except json.JSONDecodeError:
            message = body or str(e)
        return None, error_response(f"NewsData.io request failed: {message}", e.code)
    except urllib.error.URLError as e:
        current_app.logger.error("NewsData.io connection error: %s", e)
        return None, error_response(f"Could not reach NewsData.io: {e.reason}", 502)

    if payload.get("status") != "success":
        message = payload.get("results", {}).get("message") or "Unknown NewsData.io error"
        return None, error_response(message, 502)

    return payload, None


def _serialize_articles(articles):
    return [
        {
            "title": article.get("title"),
            "link": article.get("link"),
            "description": article.get("description"),
            "source_name": article.get("source_name"),
            "source_priority": article.get("source_priority"),
            "pubDate": article.get("pubDate"),
            "country": article.get("country"),
            "language": article.get("language"),
            "image_url": article.get("image_url"),
            "relevanceScore": article.get("_relevance_score"),
        }
        for article in articles
    ]


def _attach_scores(articles, filters):
    enriched = []
    for article in articles:
        row = dict(article)
        row["_relevance_score"] = score_article_relevance(
            article, filters["language_code"]
        )
        enriched.append(row)
    return enriched


def _fetch_with_fallback_strategies(filters, api_key):
    # Walk through build_news_request_strategies() until one call returns articles.
    strategies = build_news_request_strategies(filters, api_key)
    last_error = None

    for strategy in strategies:
        payload, error_response_obj = _fetch_newsdata(strategy["params"])
        if error_response_obj:
            last_error = error_response_obj
            continue

        raw_articles = payload.get("results") or []
        if raw_articles:
            current_app.logger.info(
                "News strategy %r returned %s articles",
                strategy["label"],
                len(raw_articles),
            )
            return payload, raw_articles, strategy, None

    if last_error:
        return None, None, None, last_error

    # Every strategy succeeded but came back empty.
    empty_payload = {"totalResults": 0, "results": []}
    return empty_payload, [], strategies[-1], None


# zeus_api: get_eu_energy_news(user_id)
@news_bp.route("/eu-energy", methods=["GET"])
def get_eu_energy_news():
    user_id = request.args.get("user_id", type=int)
    current_app.logger.info("GET /news/eu-energy user_id=%s", user_id)

    if not user_id:
        return error_response("Missing required query parameter: user_id", 400)

    try:
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute(
                """
                SELECT user_id, display_name, country, language
                FROM users
                WHERE user_id = %s
                """,
                (user_id,),
            )
            user = cursor.fetchone()
    except Error as e:
        current_app.logger.error("Database error in get_eu_energy_news: %s", e)
        return error_response(str(e))

    filters, error = resolve_user_news_filters(user)
    if error:
        return error_response(error, 400)

    api_key = os.getenv("NEWSDATA_API_KEY", "").strip()
    payload, raw_articles, strategy, fetch_error = _fetch_with_fallback_strategies(
        filters, api_key
    )
    if fetch_error:
        return fetch_error

    # Re-rank the raw API results before sending them to Streamlit.
    ranked = filter_and_rank_articles(raw_articles, filters)
    trimmed = _serialize_articles(_attach_scores(ranked, filters))

    return jsonify(
        {
            "totalResults": len(trimmed),
            "rawTotalResults": payload.get("totalResults", len(raw_articles)),
            "articles": trimmed,
            "titleQuery": strategy["query"],
            "queryStrategy": strategy["label"],
            "categories": strategy["params"].get("category"),
            "country": filters["country_name"],
            "countryCode": filters["country_code"],
            "language": filters["language_name"],
            "languageCode": filters["language_code"],
            "userId": user_id,
            "sourceFilter": "tiered energy query + relevance scoring",
        }
    ), 200
