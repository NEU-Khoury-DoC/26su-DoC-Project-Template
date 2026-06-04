import numpy as np
from flask import current_app
from backend.db_connection import get_db


def train():
    """
    Trains the model on clean data and stores parameters in the db

    Returns:
        dict with mse and r2
    """
    cols = ['crime_rate', 'noise_rate', 'pollution_rate', 'hpi_weight', 'deg_urb_Rural areas', 'deg_urb_Towns and suburbs']
    X = np.array(df[cols])
    y = np.array(df['happy_rate'])
 
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.3, random_state=42)
 
    scaler = StandardScaler()
    Xtrain_scaled = scaler.fit_transform(Xtrain)
    Xtest_scaled  = scaler.transform(Xtest)
 
    b = line_of_best_fit(Xtrain_scaled, ytrain)
    results = linreg_predict(Xtest_scaled, ytest, b)
 
    current_app.logger.info(f"train mse={results['mse']:.4f} r2={results['r2']:.4f}")
 
    # storing b, scaler mean, and scaler std in db
    b_str = '[' + ','.join(map(str, b)) + ']'
    scaler_mean_str = '[' + ','.join(map(str, scaler.mean_)) + ']'
    scaler_std_str = '[' + ','.join(map(str, scaler.scale_)) + ']'
 
    with get_db().cursor() as cursor:
        cursor.execute(
            '''INSERT INTO student_model_params
               (beta_vals, scaler_mean, scaler_std)
               VALUES (%s, %s, %s)''',
            (b_str, scaler_mean_str, scaler_std_str)
        )
 
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
            '''SELECT beta_vals, scaler_mean, scaler_std
               FROM student_model_params
               ORDER BY id DESC LIMIT 1'''
        )
        row = cursor.fetchone()
 
    if row is None:
        raise ValueError("No model parameters found. Run train() first.")
 
    def parse(s):
        return np.array(list(map(float, s[1:-1].split(','))))
 
    b = parse(row['beta_vals'])
    scaler_mean = parse(row['scaler_mean'])
    scaler_std = parse(row['scaler_std'])
 
    df = pd.read_csv("merged2.csv")
    df_model = (
        df.groupby(['geo', 'year'], as_index=False)
        [FEATURE_COLS + ['happy_rate']]
        .mean()
    )
 
    X = np.array(df_model[FEATURE_COLS]).astype(float)
    y = np.array(df_model['happy_rate'])
 
    _, Xtest, _, ytest = train_test_split(X, y, test_size=0.3, random_state=42)
 
    Xtest_scaled = (Xtest - scaler_mean) / scaler_std
    results = linreg_predict(Xtest_scaled, ytest, b)
 
    current_app.logger.info(f"test mse={results['mse']:.4f} r2={results['r2']:.4f}")
    return {'mse': results['mse'], 'r2': results['r2']}
 
 
def predict(crime, noise, pollution, hpi, is_rural, is_towns):
    """
    Retrieves stored model parameters from the DB and returns a predicted
    life satisfaction score for the given housing inputs.
 
    Args:
        crime (float): crime rate (raw value)
        noise (float): noise rate (raw value)
        pollution (float): pollution rate (raw value)
        hpi (float): housing price index (raw value)
        is_rural (bool): True if rural area
        is_towns (bool): True if towns/suburbs (both False = cities)
 
    Returns:
        predicted satisfaction score (float)
    """
    with get_db().cursor(dictionary=True) as cursor:
        cursor.execute(
            '''SELECT beta_vals, scaler_mean, scaler_std
               FROM student_model_params
               ORDER BY id DESC LIMIT 1'''
        )
        row = cursor.fetchone()
 
    if row is None:
        raise ValueError("No model parameters found. Run train() first.")
 
    def parse(s):
        return np.array(list(map(float, s[1:-1].split(','))))
 
    b = parse(row['beta_vals'])
    scaler_mean = parse(row['scaler_mean'])
    scaler_std = parse(row['scaler_std'])
 
    input_dict = {
        'crime_rate':                  float(crime),
        'noise_rate':                  float(noise),
        'pollution_rate':              float(pollution),
        'hpi_weight':                  float(hpi),
        'deg_urb_Rural areas':         float(is_rural),
        'deg_urb_Towns and suburbs':   float(is_towns),
    }
 
    X_input  = np.array([input_dict[col] for col in FEATURE_COLS]).astype(float)
    X_scaled = (X_input - scaler_mean) / scaler_std
 
    input_array = np.concatenate([[1.0], X_scaled])
    prediction  = float(np.dot(b, input_array))
 
    current_app.logger.info(f'student_linreg predict={prediction:.4f}')
    return prediction