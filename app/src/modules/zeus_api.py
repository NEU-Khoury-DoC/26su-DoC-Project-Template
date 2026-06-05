"""HTTP helpers for Zeus API routes used by Streamlit pages."""

import os

import requests

API_BASE = os.getenv("ZEUS_API_BASE", "http://web-api:4000")


def _get(path, params=None):
    response = requests.get(f"{API_BASE}{path}", params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def _post(path, payload):
    response = requests.post(f"{API_BASE}{path}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def _put(path, payload):
    response = requests.put(f"{API_BASE}{path}", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def _delete(path):
    response = requests.delete(f"{API_BASE}{path}", timeout=30)
    response.raise_for_status()
    return response.json() if response.content else {}


def get_users(persona):
    return _get("/users", params={"persona": persona})


def get_household_profile(user_id):
    response = requests.get(
        f"{API_BASE}/users/{user_id}/household-profile", timeout=30
    )
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def create_household_profile(user_id, profile):
    return _post(f"/users/{user_id}/household-profile", profile)


def update_household_profile(user_id, profile):
    return _put(f"/users/{user_id}/household-profile", profile)


def delete_household_profile(user_id):
    return _delete(f"/users/{user_id}/household-profile")


def get_storage_summary(country_code):
    return _get(f"/countries/{country_code}/storage/summary")


def get_storage_history(country_code):
    return _get("/stats/storage/history", params={"country": country_code})


def get_storage_winters(country_code=None):
    params = {"country": country_code} if country_code else None
    payload = _get("/stats/storage/winters", params=params)
    return payload["winters"]


def compare_storage_risk():
    return _get("/stats/storage/risk/compare")


def post_storage_risk(
    *,
    country=None,
    winter=None,
    storage_at_start,
    storage_trend_30d=None,
    storage_volatility=None,
):
    payload = {"storage_at_start": storage_at_start}
    if country is not None:
        payload["country"] = country
    if winter is not None:
        payload["winter"] = winter
    if storage_trend_30d is not None:
        payload["storage_trend_30d"] = storage_trend_30d
    if storage_volatility is not None:
        payload["storage_volatility"] = storage_volatility
    return _post("/stats/storage/risk", payload)
