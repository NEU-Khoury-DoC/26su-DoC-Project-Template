import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from flask import current_app
from backend.db_connection import get_db
from sklearn.linear_model import LinearRegression

FEATURE_COLS = [
    "immigration_count", "overburden_rate", "gdp_per_capita", "population_density", 
    "unemployment_rate", "density_unemployment", "gdp_unemployment", "density_overburden"
]

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "raw_project_models/merged_linreg.csv"))

def line_of_best_fit(X, y):
    model = LinearRegression(fit_intercept = True)
    model.fit(X, y)
    return np.concatenate([[model.intercept_], model.coef_])

def linreg_predict(X, y, b):
    X_with_intercept = np.column_stack([np.ones(len(X)), X])
    y_pred = X_with_intercept @ b
    mse = float(np.mean((y - y_pred) ** 2))
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = float(1 - ss_res / ss_tot)
    return {"mse": mse, "r2": r2}

def train():
    cols = [
    "immigration_count", "overburden_rate", "gdp_per_capita", "population_density", 
    "unemployment_rate", "density_unemployment", "gdp_unemployment", "density_overburden"
    ]
    X = np.array(df[cols])
    y = np.array(df["deprivation_rate"])

    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.3, random_state=42)

    scaler = StandardScaler()
    Xtrain_scaled = scaler.fit_transform(Xtrain)
    Xtest_scaled = scaler.transform(Xtest)

    b = line_of_best_fit(Xtrain_scaled, ytrain)
    results = linreg_predict(Xtest_scaled, ytest, b)

    current_app.logger.info(f"train mse={results['mse']:.4f} r2={results['r2']:.4f}")

    b_str = '[' + ','.join(map(str, b)) + ']'
    scaler_mean_str = '[' + ','.join(map(str, scaler.mean_)) + ']'
    scaler_std_str = '[' + ','.join(map(str, scaler.scale_)) + ']'

    with get_db().cursor() as cursor:
        cursor.execute(
            '''INSERT INTO gov_model_params
               (ga_beta_vals, ga_scaler_mean, ga_scaler_std)
               VALUES (%s, %s, %s)''',
            (b_str, scaler_mean_str, scaler_std_str)
        )
    get_db().commit()

    return {'mse': results['mse'], 'r2': results['r2']}


def test():
    """
    Retrieves stored model parameters from the DB and evaluates them
    on the held-out test set.
 
    Returns:
        dict with mse and r2
    """
    with get_db().cursor(dictionary=True) as cursor:
        cursor.execute(
            '''SELECT ga_beta_vals, ga_scaler_mean, ga_scaler_std
               FROM gov_model_params
               ORDER BY id DESC LIMIT 1'''
        )
        row = cursor.fetchone()
 
    if row is None:
        raise ValueError("No model parameters found. Run train() first.")
 
    def parse(s):
        return np.array(list(map(float, s[1:-1].split(','))))
 
    b = parse(row['ga_beta_vals'])
    scaler_mean = parse(row['ga_scaler_mean'])
    scaler_std = parse(row['ga_scaler_std'])
 
    df = pd.read_csv("merged_linreg.csv")
 
    X = np.array(df[FEATURE_COLS]).astype(float)
    y = np.array(df["deprivation_rate"])
 
    _, Xtest, _, ytest = train_test_split(X, y, test_size=0.3, random_state=42)
 
    Xtest_scaled = (Xtest - scaler_mean) / scaler_std
    results = linreg_predict(Xtest_scaled, ytest, b)
 
    current_app.logger.info(f"test mse={results['mse']:.4f} r2={results['r2']:.4f}")
    return {'mse': results['mse'], 'r2': results['r2']}
 
 
def predict(immigration_count, overburden_rate, gdp_per_capita, population_density, unemployment_rate):
    """
    Retrieves stored model parameters from the DB and returns a predicted
    housing deprivation rate given the input features.
 
    Args:
        immigration_count (float): immigration count (raw value)
        overburden_rate (float): overburden rate (raw value)
        gdp_per_capita (float): GDP per capita (raw value)
        population_density (float): population density (raw value)
        unemployment_rate (float): unemployment rate (raw value)
        density_unemployment (float): density of unemployment (raw value)
        gdp_unemployment (float): GDP of unemployment (raw value)
        density_overburden (float): density of overburden (raw value)
        is_towns (bool): True if towns/suburbs (both False = cities)
 
    Returns:
        predicted housing deprivation rate (float)
    """
    with get_db().cursor(dictionary=True) as cursor:
        cursor.execute(
            '''SELECT ga_beta_vals, ga_scaler_mean, ga_scaler_std
               FROM gov_model_params
               ORDER BY id DESC LIMIT 1'''
        )
        row = cursor.fetchone()

    if row is None:
        raise ValueError("No model parameters found. Run train() first.")
 
    def parse(s):
        return np.array(list(map(float, s[1:-1].split(','))))
 
    b = parse(row['ga_beta_vals'])
    scaler_mean = parse(row['ga_scaler_mean'])
    scaler_std = parse(row['ga_scaler_std'])
 
    input_dict = {
        "immigration_count": immigration_count,
        "overburden_rate": overburden_rate,
        "gdp_per_capita": gdp_per_capita,
        "population_density": population_density,
        "unemployment_rate": unemployment_rate,
        "density_unemployment": population_density * unemployment_rate,
        "gdp_unemployment": gdp_per_capita * unemployment_rate,
        "density_overburden": population_density * overburden_rate
    }
 
    X_input  = np.array([input_dict[col] for col in FEATURE_COLS]).astype(float)
    X_scaled = (X_input - scaler_mean) / scaler_std
 
    input_array = np.concatenate([[1.0], X_scaled])
    prediction  = float(np.dot(b, input_array))
 
    current_app.logger.info(f'government_linreg predict={prediction:.4f}')
    return prediction