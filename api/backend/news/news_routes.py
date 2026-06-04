import json
import os
import urllib.error
import urllib.parse
import urllib.request

from flask import Blueprint, current_app, jsonify

from backend.utils import error_response

news_bp = Blueprint("news", __name__)

NEWSDATA_BASE_URL = "https://newsdata.io/api/1/latest"

# NewsData.io allows up to 5 countries per request on free/basic plans.
EU_SAMPLE_COUNTRIES = "de,fr,it,es,be"

# Free/Basic plans limit q to 100 chars; EU scope comes from the country filter.
ENERGY_QUERY = (
    "energy, electricity, EU"
)


@news_bp.route("/eu-energy", methods=["GET"])
def get_eu_energy_news():
    """Fetch latest EU energy news via NewsData.io."""
    current_app.logger.info("GET /news/eu-energy")

    api_key = os.getenv("NEWSDATA_API_KEY", "").strip()
    if not api_key:
        return error_response(
            "NewsData.io API key is not configured. Set NEWSDATA_API_KEY in api/.env.",
            503,
        )

    params = urllib.parse.urlencode(
        {
            "apikey": api_key,
            "q": ENERGY_QUERY,
            "country": EU_SAMPLE_COUNTRIES,
            "sort": "source",
            "datatype": "news",
        }
    )
    url = f"{NEWSDATA_BASE_URL}?{params}"

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
        return error_response(f"NewsData.io request failed: {message}", e.code)
    except urllib.error.URLError as e:
        current_app.logger.error("NewsData.io connection error: %s", e)
        return error_response(f"Could not reach NewsData.io: {e.reason}", 502)

    if payload.get("status") != "success":
        message = payload.get("results", {}).get("message") or "Unknown NewsData.io error"
        return error_response(message, 502)

    articles = payload.get("results") or []

    # Lower source_priority values indicate more reputable domains in NewsData.io.
    articles.sort(key=lambda article: article.get("source_priority") or 999_999)

    trimmed = [
        {
            "title": article.get("title"),
            "link": article.get("link"),
            "description": article.get("description"),
            "source_name": article.get("source_name"),
            "source_priority": article.get("source_priority"),
            "pubDate": article.get("pubDate"),
            "country": article.get("country"),
            "image_url": article.get("image_url"),
        }
        for article in articles
    ]

    return jsonify(
        {
            "totalResults": payload.get("totalResults", len(trimmed)),
            "articles": trimmed,
            "query": ENERGY_QUERY,
            "countries": EU_SAMPLE_COUNTRIES,
            "sourceFilter": "prioritydomain=top (top 10% domains), sorted by source authority",
        }
    ), 200
