"""
electricity_price_model.py — EU Electricity Price Forecast (ML1)

Predicts 30-day electricity prices for a given EU country.
Weights stored in ml1_price_forecast_model table in the database.

Prediction formula: wTx + intercept
  w = vector of 42 weights loaded from DB
  x = input vector of lag features + rolling stats + month/dow/country dummies
"""
import numpy as np
import pandas as pd
from flask import current_app
from backend.db_connection import get_db


def train():
    """
    Model is trained in the Jupyter notebook (datasets/entsoe/entsoe.ipynb).
    Weights are inserted into ml1_price_forecast_model table manually.
    To retrain: run Step 4 in the notebook and update the DB insert statement.
    """
    pass


def test():
    """
    Model evaluation (MAE, RMSE, R²) is performed in the Jupyter notebook.
    Current performance: R²=0.608, MAE=17.68, RMSE=23.21
    """
    pass


def _get_weights():
    """
    Fetches the most recent model weights and intercept from ml1_price_forecast_model.
    Returns a dict of {column_name: value}.
    """
    with get_db().cursor(dictionary=True) as cursor:
        cursor.execute(
            'SELECT * FROM ml1_price_forecast_model ORDER BY model_id DESC LIMIT 1'
        )
        row = cursor.fetchone()

    if row is None:
        raise ValueError("No ML1 weights found in the database.")

    current_app.logger.info('ML1 weights loaded from DB')
    return row


def _get_recent_prices(country_code):
    """
    Fetches the most recent 30 days of prices for the given country.
    Returns list of prices oldest to most recent, and the last date.
    """
    with get_db().cursor(dictionary=True) as cursor:
        cursor.execute(
            'SELECT date, avg_price_eur_mwh FROM daily_prices '
            'WHERE country = %s ORDER BY date DESC LIMIT 30',
            (country_code,)
        )
        rows = cursor.fetchall()

    if not rows:
        raise ValueError(f"No price data found for country: {country_code}")

    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return list(df["avg_price_eur_mwh"]), pd.Timestamp(df["date"].iloc[-1])


def _build_x(last_prices, next_date, country_code):
    """
    Builds the x input vector for one prediction step.

    Args:
        last_prices  (list): recent price history, most recent last
        next_date    (pd.Timestamp): the date being predicted
        country_code (str): two-letter country code e.g. "DE"

    Returns:
        np.array: x vector of 42 features in correct order
    """
    # Lag features
    lag_1 = last_prices[-1]
    lag_2 = last_prices[-2]
    lag_3 = last_prices[-3]
    lag_4 = last_prices[-4]
    lag_5 = last_prices[-5]
    lag_6 = last_prices[-6]
    lag_7 = last_prices[-7]

    # Rolling features
    rolling_7d_mean  = float(np.mean(last_prices[-7:]))
    rolling_30d_mean = float(np.mean(last_prices[-30:])) if len(last_prices) >= 30 else float(np.mean(last_prices))
    rolling_7d_std   = float(np.std(last_prices[-7:]))
    price_vs_7d_avg  = lag_1 / rolling_7d_mean if rolling_7d_mean != 0 else 1.0

    # Month dummies (drop_first=True drops month_1)
    month_2  = 1 if next_date.month == 2  else 0
    month_3  = 1 if next_date.month == 3  else 0
    month_4  = 1 if next_date.month == 4  else 0
    month_5  = 1 if next_date.month == 5  else 0
    month_6  = 1 if next_date.month == 6  else 0
    month_7  = 1 if next_date.month == 7  else 0
    month_8  = 1 if next_date.month == 8  else 0
    month_9  = 1 if next_date.month == 9  else 0
    month_10 = 1 if next_date.month == 10 else 0
    month_11 = 1 if next_date.month == 11 else 0
    month_12 = 1 if next_date.month == 12 else 0

    # Dayofweek dummies (drop_first=True drops dow_0)
    dow_1 = 1 if next_date.dayofweek == 1 else 0
    dow_2 = 1 if next_date.dayofweek == 2 else 0
    dow_3 = 1 if next_date.dayofweek == 3 else 0
    dow_4 = 1 if next_date.dayofweek == 4 else 0
    dow_5 = 1 if next_date.dayofweek == 5 else 0
    dow_6 = 1 if next_date.dayofweek == 6 else 0

    # Country dummies (drop_first=True drops AT)
    country_BE = 1 if country_code == "BE" else 0
    country_BG = 1 if country_code == "BG" else 0
    country_CZ = 1 if country_code == "CZ" else 0
    country_DE = 1 if country_code == "DE" else 0
    country_ES = 1 if country_code == "ES" else 0
    country_FR = 1 if country_code == "FR" else 0
    country_HR = 1 if country_code == "HR" else 0
    country_HU = 1 if country_code == "HU" else 0
    country_LV = 1 if country_code == "LV" else 0
    country_NL = 1 if country_code == "NL" else 0
    country_PL = 1 if country_code == "PL" else 0
    country_PT = 1 if country_code == "PT" else 0
    country_RO = 1 if country_code == "RO" else 0
    country_SK = 1 if country_code == "SK" else 0

    # Build x vector in exact feature order matching w
    x = np.array([
        lag_1, lag_2, lag_3, lag_4, lag_5, lag_6, lag_7,
        rolling_7d_mean, rolling_30d_mean, rolling_7d_std, price_vs_7d_avg,
        month_2, month_3, month_4, month_5, month_6,
        month_7, month_8, month_9, month_10, month_11, month_12,
        dow_1, dow_2, dow_3, dow_4, dow_5, dow_6,
        country_BE, country_BG, country_CZ, country_DE, country_ES,
        country_FR, country_HR, country_HU, country_LV, country_NL,
        country_PL, country_PT, country_RO, country_SK
    ])

    return x


def predict(country_code, days=30):
    """
    Generates a 30-day electricity price forecast for the given country.

    Args:
        country_code (str): two-letter country code e.g. "DE", "BE"
        days (int): number of days to forecast (default 30)

    Returns:
        list[dict]: list of {date, predicted_price_eur_mwh}
    """
    weights = _get_weights()
    last_prices, last_date = _get_recent_prices(country_code)

    # Build w vector in exact same order as x
    w = np.array([
        weights["weight_lag_1"], weights["weight_lag_2"], weights["weight_lag_3"],
        weights["weight_lag_4"], weights["weight_lag_5"], weights["weight_lag_6"],
        weights["weight_lag_7"],
        weights["weight_rolling_7d_mean"], weights["weight_rolling_30d_mean"],
        weights["weight_rolling_7d_std"], weights["weight_price_vs_7d_avg"],
        weights["weight_month_2"], weights["weight_month_3"], weights["weight_month_4"],
        weights["weight_month_5"], weights["weight_month_6"], weights["weight_month_7"],
        weights["weight_month_8"], weights["weight_month_9"], weights["weight_month_10"],
        weights["weight_month_11"], weights["weight_month_12"],
        weights["weight_dow_1"], weights["weight_dow_2"], weights["weight_dow_3"],
        weights["weight_dow_4"], weights["weight_dow_5"], weights["weight_dow_6"],
        weights["weight_country_BE"], weights["weight_country_BG"], weights["weight_country_CZ"],
        weights["weight_country_DE"], weights["weight_country_ES"], weights["weight_country_FR"],
        weights["weight_country_HR"], weights["weight_country_HU"], weights["weight_country_LV"],
        weights["weight_country_NL"], weights["weight_country_PL"], weights["weight_country_PT"],
        weights["weight_country_RO"], weights["weight_country_SK"]
    ])

    intercept = float(weights["intercept"])
    predictions = []

    for _ in range(days):
        next_date = last_date + pd.Timedelta(days=1)

        # Build x
        x = _build_x(last_prices, next_date, country_code)

        # wTx + intercept
        pred = float(w.T @ x) + intercept

        predictions.append({
            "date": str(next_date.date()),
            "predicted_price_eur_mwh": round(pred, 2)
        })

        # Roll forward
        last_prices.append(pred)
        last_date = next_date

    current_app.logger.info(f'ML1 forecast for {country_code}: {days} days generated')
    return predictions
