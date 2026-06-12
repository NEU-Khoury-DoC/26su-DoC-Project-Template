"""
model03.py — Crop type KNN predictor

Predicts what type of crop to plant from:
  - N:               soil nitrogen content
  - P:               soil phosphorus content
  - K:               soil potassium content
  - TYPE_OF_CROP:    categorical crop category (e.g. 'cereals')
  - TEMPERATURE:     average temperature
  - SEASON:          growing season (e.g. 'Monsoon (Kharif)', 'Winter (Rabi)')
  - SOWN:            sowing month (e.g. 'Jun')
  - HARVESTED:       harvest month (e.g. 'Oct')
  - WATER_SOURCE:    irrigation source (e.g. 'rainfed')
  - RELATIVE_HUMIDITY: relative humidity (%)

Hard-coded training averages:
  - CROPDURATION:    109.347
  - WATERREQUIRED:   887.26
  - SOIL_PH:         6.624
  - SOIL:            'sandy Loamy soil'

No model parameters stored in the DB because KNN is unsupervised.
Scaler parameters (means, stds) and training data are stored in the DB.

Scaling is done via StandardScaler
Categorical features are one-hot encoded and appended unscaled.
cosine similarity.
"""

import json
from collections import Counter

import numpy as np
from flask import current_app
from backend.db_connection import get_db


# ------------------------------------------------------------
# Hard-coded averages used to fill hidden features at predict time
# ------------------------------------------------------------
_CROPDURATION_AVG  = 109.347
_WATERREQUIRED_AVG = 887.26
_SOIL_PH_AVG       = 6.624
_SOIL_AVG          = 'sandy Loamy soil'

# Order has to match column order used when the scaler was fitted.
# SOIL_PH is first (it sits before CROPDURATION in the source CSV) and is
# always filled with the training average at predict time.
_CONTINUOUS_COLS = [
    'SOIL_PH',
    'CROPDURATION',
    'TEMPERATURE',
    'WATERREQUIRED',
    'RELATIVE_HUMIDITY',
    'N',
    'P',
    'K',
]

# one-hot columns, prefix
_OHE_PREFIXES = ('TYPE_OF_CROP_', 'SOIL_', 'SOWN_', 'HARVESTED_', 'WATER_SOURCE_', 'SEASON')

# One-hot columns hardcoded, (MUST BE IN SME ORDER AS TRAINING DATA!!)

_OHE_COLS = [
    # TYPE_OF_CROP (0-9)
    'TYPE_OF_CROP_Root&tuber', 'TYPE_OF_CROP_bulbvegetables', 'TYPE_OF_CROP_cereals',
    'TYPE_OF_CROP_colecrops', 'TYPE_OF_CROP_fibre crop', 'TYPE_OF_CROP_millets',
    'TYPE_OF_CROP_oil seeds', 'TYPE_OF_CROP_pulses', 'TYPE_OF_CROP_sugar crops',
    'TYPE_OF_CROP_vegetables',
    # SOIL (10-41)
    'SOIL_Alluvial soil', 'SOIL_Black Soil', 'SOIL_Clay soil', 'SOIL_Laterite soil',
    'SOIL_Loamy soil', 'SOIL_Red soil', 'SOIL_Sandy soil', 'SOIL_Sandy soil',
    'SOIL_black cotton soil', 'SOIL_brown Loamy soil', 'SOIL_clay Loamy soil',
    'SOIL_cotton soil', 'SOIL_deep soil', 'SOIL_friable soil', 'SOIL_heavy Black Soil',
    'SOIL_heavy soil', 'SOIL_light Loamy soil', 'SOIL_light soi', 'SOIL_loamy soil',
    'SOIL_medium Black Soil', 'SOIL_red Loamy soil', 'SOIL_red lateritic Loamy soil',
    'SOIL_rich red Loamy soil', 'SOIL_salty clay Loamy soil', 'SOIL_sandy Loamy soil',
    'SOIL_sandy clay Loamy soil', 'SOIL_sandy loamy soil', 'SOIL_shallow Black Soil',
    'SOIL_silty Loamy soil', 'SOIL_well-drained loamy soil', 'SOIL_well-drained soil',
    'SOIL_well-grained deep loamy moist soil',
    # SOWN (42-49)
    'SOWN_Apr', 'SOWN_Dec', 'SOWN_Jul', 'SOWN_Jun', 'SOWN_Mar', 'SOWN_May', 'SOWN_Nov',
    'SOWN_Oct',
    # HARVESTED (50-56)
    'HARVESTED_Apr', 'HARVESTED_Jul', 'HARVESTED_Jun', 'HARVESTED_Mar', 'HARVESTED_May',
    'HARVESTED_Oct', 'HARVESTED_Sep',
    # WATER_SOURCE (57-58)
    'WATER_SOURCE_irrigated', 'WATER_SOURCE_rainfed',
    # SEASON (59-61)
    'SEASON_Summer (Zaid)', 'SEASON_Monsoon (Kharif)', 'SEASON_Winter (Rabi)',
]
#dictionary
_OHE_INDEX = {name: i for i, name in enumerate(_OHE_COLS)}


#scalar params from db
def _get_scaler_params():
    """
    Fetches the most-recent StandardScaler parameters from model3_scaler.

    Returns:
        tuple[np.ndarray, np.ndarray]: (means, stds), each shape (n_continuous,)
    Raises:
            ValueError: if no parameters exist in the database yet.
    """
    with get_db().cursor(dictionary=True) as cursor:
        cursor.execute(
            'SELECT feature_means, feature_stds '
            'FROM model3_scaler '
            'ORDER BY id DESC LIMIT 1'
        )
        row = cursor.fetchone()

    if row is None:
        raise ValueError("No model3 params found in the database.")

    means = np.array(json.loads(row['feature_means']))
    stds  = np.array(json.loads(row['feature_stds']))
    current_app.logger.info(f'model03 scaler loaded: means={means}, stds={stds}')
    return means, stds


# fetch training 
def _get_training_data():
    """
    Fetches the training matrix and labels from the DB.
    Rows are stored as JSON arrays, labels as plain strings.

    Returns:
        tuple[np.ndarray, np.ndarray]:
            X_train  shape (n_samples, n_features) already scaled + OHE
            y_train  shape (n_samples,) crop name strings

    Raises:
        ValueError: if no training data exists yet.
    """
    with get_db().cursor(dictionary=True) as cursor:
        cursor.execute(
            'SELECT feature_vector, crop_label '
            'FROM model3_training_data '
            'ORDER BY row_id ASC'
        )
        rows = cursor.fetchall()

    if not rows:
        raise ValueError('No model3 training data found in the database.')

    X_train = np.array([json.loads(r['feature_vector']) for r in rows], dtype=float)
    y_train = np.array([r['crop_label'] for r in rows])
    current_app.logger.info(f'model03 training data: {X_train.shape}')
    return X_train, y_train


# ------------------------------------------------------------
# KNN with cosine similarity (vectorised inner loop)
# ------------------------------------------------------------

def _knn_cos(X_train, y_train, X_test, k):
    """
    K-nearest-neighbours classifier using cosine similarity.

    Args:
        X_train  (np.ndarray): shape (n_train, n_features)
        y_train  (np.ndarray): shape (n_train,) - string labels
        X_test   (np.ndarray): shape (n_test,  n_features)
        k        (int):  number of neighbours

    Returns:
        list[np.ndarray]:
            neighbour_labels  - list of length n_test, each element is an array
                                of the k neighbour labels ordered closest-first
                                (highest cosine similarity first)
    """
    train_norms = np.linalg.norm(X_train, axis=1, keepdims=True)
    X_train_normed = X_train / np.where(train_norms == 0, 1, train_norms)

    neighbour_labels = []

    for test_point in X_test:
        norm = np.linalg.norm(test_point)
        test_normed = test_point / (norm if norm != 0 else 1)

        similarities  = test_normed @ X_train_normed.T          # (n_train,)
        # top-k indices, ordered closest (highest similarity) first
        neighbour_idx = np.argsort(similarities)[-k:][::-1]
        neighbour_labels.append(y_train[neighbour_idx])

    return neighbour_labels


# ------------------------------------------------------------
# Public predict function called by route handlers
# ------------------------------------------------------------

def predict(N, P, K, TYPE_OF_CROP, TEMPERATURE, SEASON, SOWN, HARVESTED,
            WATER_SOURCE, RELATIVE_HUMIDITY,
            CROPDURATION=_CROPDURATION_AVG, WATERREQUIRED=_WATERREQUIRED_AVG,
            k=5):
    """
    Returns the crops of the k nearest neighbours given the input features.

    Args:
        N                  (str | float): soil nitrogen
        P                  (str | float): soil phosphorus
        K                  (str | float): soil potassium
        TYPE_OF_CROP       (str):         e.g. 'cereals'
        TEMPERATURE        (str | float): average temperature (°C)
        SEASON             (str):         e.g. 'Monsoon (Kharif)'
        SOWN               (str):         sowing month, e.g. 'Jun'
        HARVESTED          (str):         harvest month, e.g. 'Oct'
        WATER_SOURCE       (str):         e.g. 'rainfed'
        RELATIVE_HUMIDITY  (str | float): relative humidity (%)
        CROPDURATION       (str | float): crop growth duration (days).
                                          Defaults to the training average.
        WATERREQUIRED      (str | float): water requirement (mm).
                                          Defaults to the training average.
        k                  (int):         number of KNN neighbours (default 5)

    Note:
        SOIL_PH is a model feature but is never collected from the caller; it
        is always filled with the training average (_SOIL_PH_AVG).

    Returns:
        list[str]: recommended crop names, deduplicated and ranked most-likely
                   first (by neighbour vote count, ties broken by closeness).

    Raises:
        ValueError: if a categorical value is not in the stored OHE columns,
                    or if required DB artefacts are missing.
    """
    # load db stuff
    means, stds  = _get_scaler_params()
    X_train, y_train = _get_training_data()

    # -cont feat vect.
    x_cont = np.array([
        float(_SOIL_PH_AVG),
        float(CROPDURATION),
        float(TEMPERATURE),
        float(WATERREQUIRED),
        float(RELATIVE_HUMIDITY),
        float(N),
        float(P),
        float(K),
    ])

    # scale using training statistics
    x_scaled = (x_cont - means) / stds  # shape (n_continuous,)

    # --- build OHE vector ---
    ohe_input = np.zeros(len(_OHE_INDEX), dtype=float)

    categorical_inputs = {
        'TYPE_OF_CROP': TYPE_OF_CROP,
        'SEASON':       SEASON,
        'SOWN':         SOWN,
        'HARVESTED':    HARVESTED,
        'WATER_SOURCE': WATER_SOURCE,
    }

    for prefix, value in categorical_inputs.items():
        col_name = f'{prefix}_{value}'
        if col_name not in _OHE_INDEX:
            raise ValueError(
                f"Unknown value '{value}' for '{prefix}'. "
                f"Expected one of: {[c for c in _OHE_COLS if c.startswith(prefix)]}"
            )
        ohe_input[_OHE_INDEX[col_name]] = 1.0

    # concatenate and predict
    new_X = np.concatenate([x_scaled, ohe_input]).reshape(1, -1)  # (1, n_features)

    # labels of the k nearest neighbours, ordered closest-first
    neighbour_labels = [str(label) for label in _knn_cos(X_train, y_train, new_X, k)[0]]

    # deduplicate and rank: most frequent first, ties broken by closeness
    vote_counts = Counter(neighbour_labels)
    predictions = sorted(
        vote_counts,
        key=lambda crop: (-vote_counts[crop], neighbour_labels.index(crop)),
    )

    current_app.logger.info(
        f'model03.predict(N={N}, P={P}, K={K}, TYPE_OF_CROP={TYPE_OF_CROP}, '
        f'TEMP={TEMPERATURE}, SEASON={SEASON}, k={k}) -> {predictions}'
    )
    return predictions