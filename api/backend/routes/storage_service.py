"""Gas storage data access — reads from MySQL, not CSV files."""

from functools import lru_cache
from pathlib import Path

import joblib

FEATURES = ["storage_at_start", "storage_trend_30d", "storage_volatility"]
STRESS_THRESHOLD = 30

CODE_TO_NAME = {
    "AT": "Austria", "BE": "Belgium", "BG": "Bulgaria", "HR": "Croatia",
    "CZ": "Czech Republic", "DK": "Denmark", "FR": "France", "DE": "Germany",
    "HU": "Hungary", "IT": "Italy", "LV": "Latvia", "NL": "Netherlands",
    "PL": "Poland", "PT": "Portugal", "RO": "Romania", "SK": "Slovakia",
    "ES": "Spain",
}
NAME_TO_CODE = {name: code for code, name in CODE_TO_NAME.items()}

MODEL_PATH = Path(__file__).resolve().parents[1] / "ml_models" / "gas_model.pkl"


def normalize_country_code(code):
    return code.strip().upper()


def country_name(code):
    return CODE_TO_NAME.get(normalize_country_code(code))


def fetch_daily_history(cursor, country_code):
    cursor.execute(
        """
        SELECT gas_day, full_pct
        FROM gas_storage_daily
        WHERE country_code = %s
        ORDER BY gas_day
        """,
        (normalize_country_code(country_code),),
    )
    return cursor.fetchall()


def fetch_winters(cursor, country_code=None):
    if country_code:
        cursor.execute(
            """
            SELECT country_code, winter_year, min_winter_full, days,
                   storage_stress, storage_at_start, storage_trend_30d,
                   storage_volatility
            FROM gas_storage_winters
            WHERE country_code = %s
            ORDER BY winter_year
            """,
            (normalize_country_code(country_code),),
        )
    else:
        cursor.execute(
            """
            SELECT country_code, winter_year, min_winter_full, days,
                   storage_stress, storage_at_start, storage_trend_30d,
                   storage_volatility
            FROM gas_storage_winters
            ORDER BY country_code, winter_year
            """
        )
    return cursor.fetchall()


def fetch_latest_winter(cursor, country_code):
    cursor.execute(
        """
        SELECT country_code, winter_year, min_winter_full, days,
               storage_stress, storage_at_start, storage_trend_30d,
               storage_volatility
        FROM gas_storage_winters
        WHERE country_code = %s
        ORDER BY winter_year DESC
        LIMIT 1
        """,
        (normalize_country_code(country_code),),
    )
    return cursor.fetchone()


def fetch_latest_daily(cursor, country_code):
    cursor.execute(
        """
        SELECT gas_day, full_pct
        FROM gas_storage_daily
        WHERE country_code = %s
        ORDER BY gas_day DESC
        LIMIT 1
        """,
        (normalize_country_code(country_code),),
    )
    return cursor.fetchone()


def fetch_daily_on_or_before(cursor, country_code, gas_day):
    cursor.execute(
        """
        SELECT gas_day, full_pct
        FROM gas_storage_daily
        WHERE country_code = %s AND gas_day <= %s
        ORDER BY gas_day DESC
        LIMIT 1
        """,
        (normalize_country_code(country_code), gas_day),
    )
    return cursor.fetchone()


def winter_summary(cursor, country_code):
    winters = fetch_winters(cursor, country_code)
    if not winters:
        return None

    stress_count = sum(int(row["storage_stress"]) for row in winters)
    worst_row = min(winters, key=lambda row: float(row["min_winter_full"]))
    return {
        "stressed_winters": stress_count,
        "total_winters": len(winters),
        "worst_winter_min": float(worst_row["min_winter_full"]),
        "worst_winter_year": int(worst_row["winter_year"]),
    }


def latest_winter_per_country(cursor):
    cursor.execute(
        """
        SELECT w.*
        FROM gas_storage_winters w
        INNER JOIN (
            SELECT country_code, MAX(winter_year) AS max_winter
            FROM gas_storage_winters
            GROUP BY country_code
        ) latest
        ON w.country_code = latest.country_code
        AND w.winter_year = latest.max_winter
        ORDER BY w.country_code
        """
    )
    return cursor.fetchall()


def serialize_winter(row):
    return {
        "country": row["country_code"],
        "country_name": CODE_TO_NAME.get(row["country_code"], row["country_code"]),
        "winter": int(row["winter_year"]),
        "min_winter_full": float(row["min_winter_full"]),
        "days": row["days"],
        "storage_stress": int(row["storage_stress"]),
        "storage_at_start": float(row["storage_at_start"]),
        "storage_trend_30d": float(row["storage_trend_30d"]),
        "storage_volatility": float(row["storage_volatility"]),
    }


@lru_cache(maxsize=1)
def load_gas_model():
    return joblib.load(MODEL_PATH)


def predict_risk(storage_at_start, storage_trend_30d, storage_volatility):
    model = load_gas_model()
    features = [[storage_at_start, storage_trend_30d, storage_volatility]]
    risk_prob = float(model.predict_proba(features)[0][1])
    return {
        "at_risk": bool(model.predict(features)[0]),
        "risk_prob": risk_prob,
    }
