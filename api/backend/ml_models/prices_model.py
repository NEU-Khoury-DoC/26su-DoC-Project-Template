"""
model01.py demonstrates how to store model parameters in the database
and retrieve them at prediction time via a REST route.
"""
import numpy as np
from flask import current_app
from backend.db_connection import get_db
import json


def train():
    """
    Placeholder for a training routine. Could be triggered from an
    admin route to retrain the model and store new parameters in the DB.
    """
    return 'Training the model'


def test():
    return 'Testing the model'

# ------------------------------------------------------------
# Internal helpers — fetch the latest beta vector from the DB.
# Also fetch the scaler parameters that are stored in the DB.
# Kept private (leading underscore) so routes import the public
# functions below rather than the raw DB call.
# ------------------------------------------------------------
def _get_params():
    """
    Fetches the most recent parameter vector from price_params.

    Returns:
        np.ndarray: 1-D array of [intercept, coef1, coef2, ...]

    Raises:
        ValueError: if no parameters exist in the database yet.
    """
    with get_db().cursor(dictionary=True) as cursor:
        cursor.execute(
            'SELECT beta_vals FROM price_params ORDER BY sequence_number DESC LIMIT 1'
        )
        row = cursor.fetchone()

    if row is None:
        raise ValueError("No crop price model parameters found in the database.")

    params = np.array(json.loads(row['beta_vals']))
    current_app.logger.info(f'crop_price_model params loaded: {params}')
    return params


def _get_scaler_params():
    """
    Fetches the scaler means and stds from price_scaler.
    Order: [temperature, precipitation, precip_squared, price_lag1, price_lag2]
    """
    with get_db().cursor(dictionary=True) as cursor:
        cursor.execute(
            'SELECT feature_means, feature_stds FROM price_scaler '
            'ORDER BY sequence_number DESC LIMIT 1'
        )
        row = cursor.fetchone()

    if row is None:
        raise ValueError("No crop price scaler parameters found in the database.")

    means = np.array(json.loads(row['feature_means']))
    stds = np.array(json.loads(row['feature_stds']))
    current_app.logger.info(f'crop_price_model scalers loaded: {means, stds}')
    return means, stds

def _get_weather(country):
    """
    Fetches average temperature and precipitation for a given country.
    """
    with get_db().cursor(dictionary=True) as cursor:
        cursor.execute(
            f'SELECT AVG(temperature_2m_mean) as temp, AVG(precipitation_sum) as precip FROM WeatherData WHERE geo = "{country}";'
        )
        row = cursor.fetchone()

    if row is None or row['temp'] is None:
        raise ValueError(f"No weather data found for country: {country}")

    current_app.logger.info(f'Weather data loaded for country: {country}')
    return float(row['temp']), float(row['precip'])


def _get_lag_prices(country, crop):
    """
    Fetches the two most recent selling prices for a crop/country combo.
    """
    with get_db().cursor(dictionary=True) as cursor:
        cursor.execute(
            f'SELECT selling_price FROM CropPrices WHERE geo = "{country}" AND prod_veg = "{crop}" ORDER BY year DESC LIMIT 2'
        )
        rows = cursor.fetchall()

    if len(rows) < 2:
        raise ValueError(f"Not enough price history for {crop} in {country}")

    current_app.logger.info(f'Price history data loaded for country, crop: {(country, crop)}')

    return float(rows[0]['selling_price']), float(rows[1]['selling_price'])


def _build_feature_vector(crop, country, scaled_numerics):
    """
    Builds the full feature vector matching the training column order:
    [1.0, temp, precip, lag1, lag2, precip_sq, crop dummies..., country dummies...]

    These lists must match exactly what get_dummies produced during training
    (drop_first=True drops the first category alphabetically).
    """
    all_crops = ['Durum wheat', 'Feed barley', 'Rye', 'Soft wheat']  # minus first alphabetically
    all_countries = ['Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia',
                     'Denmark', 'Estonia', 'Finland', 'Germany', 'Greece',
                     'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania',
                     'Luxembourg', 'Netherlands', 'Poland', 'Portugal',
                     'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden']

    crop_onehot = [1.0 if crop == c else 0.0 for c in all_crops]
    country_onehot = [1.0 if country == c else 0.0 for c in all_countries]

    return np.array([1.0] + list(scaled_numerics) + crop_onehot + country_onehot)


def predict(crop, country):
    """
    Returns a predicted selling price for a given crop and country.

    Args:
        crop    (str): crop type e.g. 'Soft wheat'
        country (str): country name e.g. 'Austria'

    Returns:
        float: predicted selling price in EUR/100kg

    Raises:
        ValueError: if crop/country not found in DB, or no params in DB.
    """
    params = _get_params()
    means, stds = _get_scaler_params()

    temperature, precipitation = _get_weather(country)
    price_lag1, price_lag2 = _get_lag_prices(country, crop)

    # compute derived feature
    precip_squared = precipitation ** 2

    # scale numeric features in same order as training
    raw = np.array([temperature, precipitation, price_lag1, price_lag2, precip_squared])
    scaled = (raw - means) / stds

    feature_vec = _build_feature_vector(crop, country, scaled)
    prediction = float(params.T @ feature_vec)

    current_app.logger.info(
        f'crop_price_model.predict({crop}, {country}) -> {prediction:.2f}'
    )
    return prediction