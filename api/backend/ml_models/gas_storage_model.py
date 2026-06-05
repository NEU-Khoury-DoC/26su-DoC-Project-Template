import math


def predict_risk(weights, storage_at_start, storage_trend_30d, storage_volatility):
    z = (
        weights["intercept"]
        + weights["weight_storage_at_start"] * storage_at_start
        + weights["weight_storage_trend_30d"] * storage_trend_30d
        + weights["weight_storage_volatility"] * storage_volatility
    )
    risk_prob = 1.0 / (1.0 + math.exp(-z))
    return {
        "at_risk": risk_prob >= 0.5,
        "risk_prob": risk_prob,
    }
