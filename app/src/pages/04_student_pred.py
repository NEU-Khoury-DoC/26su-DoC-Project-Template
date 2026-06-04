import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.title("Housing Satisfaction Predictor")
st.write("Adjust the sliders to your ideal housing conditions and see your predicted life satisfaction score.")



crime      = st.slider("Crime & Vandalism (0 = safest, 100 = highest)",     0, 100, 25)
noise      = st.slider("Noise Levels (0 = quietest, 100 = noisiest)",       0, 100, 25)
pollution  = st.slider("Pollution & Grime (0 = cleanest, 100 = most)",      0, 100, 25)
hpi        = st.slider("Housing Price Growth (0 = falling, 100 = rising)",  0, 100, 40)

urb = st.radio(
    "Area type",
    options=["Cities", "Towns & Suburbs", "Rural Areas"],
    horizontal=True
)

is_rural = urb == "Rural Areas"
is_towns = urb == "Towns & Suburbs"


RAW_RANGES = {
    'crime_rate':     (0.0,  37.3),
    'noise_rate':     (3.2,  55.9),
    'pollution_rate': (1.6,  43.1),
    'hpi_weight':     (-9.1, 14.3),
}

def pct_to_raw(pct, col):
    low, high = RAW_RANGES[col]
    return low + (pct / 100) * (high - low)



if st.button("Predict"):
    payload = {
        "crime":     pct_to_raw(crime,     'crime_rate'),
        "noise":     pct_to_raw(noise,     'noise_rate'),
        "pollution": pct_to_raw(pollution, 'pollution_rate'),
        "hpi":       pct_to_raw(hpi,       'hpi_weight'),
        "is_rural":  is_rural,
        "is_towns":  is_towns,
    }

    try:
        response = requests.post("http://web-api:4000/housing/student/predict", json=payload)
        response.raise_for_status()
        score = round(response.json().get("prediction", 0), 1)
        score_display = max(1.0, min(10.0, score))

        st.metric(label="Predicted Life Satisfaction Score", value=f"{score_display} / 10")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend. Make sure the Flask server is running on port 4000.")
    except Exception as e:
        st.error(f"Something went wrong: {e}")