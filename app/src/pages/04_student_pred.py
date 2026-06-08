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

response = requests.post("http://web-api:4000/housing/student/train")

st.title("Housing Satisfaction Predictor")
SideBarLinks()
st.write("Set your comfortability levels with these housing conditions to see your predicted life satisfaction score in different countries across Europe.")
st.divider()


# st.subheader("Start from a country (optional)")

# try:
#     countries_resp = requests.get("http://web-api:4000/housing/country")
#     countries_resp.raise_for_status()
#     country_list = [c['country_name'] for c in countries_resp.json()]
# except:
#     country_list = []

# selected_country = st.selectbox(
#     "Select a country to pre-fill with real values",
#     options=["— None —"] + sorted(country_list),
#     key="country_select"
# )

# if selected_country != "— None —":
#     try:
#         stats_resp = requests.get(
#             "http://web-api:4000/housing/social-indicator-stats",
#             params={"country": selected_country}
#         )
#         stats_resp.raise_for_status()
#         stats = stats_resp.json()

#         def raw_to_pct(val, col):
#             low, high = RAW_RANGES[col]
#             return int(((val - low) / (high - low)) * 100)

#         for s in stats:
#             name = s.get('name', '').lower()
#             val  = s.get('value', 0)
#             if 'crime' in name:
#                 st.session_state['crime'] = max(0, min(100, raw_to_pct(val, 'crime_rate')))
#             elif 'noise' in name:
#                 st.session_state['noise'] = max(0, min(100, raw_to_pct(val, 'noise_rate')))
#             elif 'pollution' in name:
#                 st.session_state['pollution'] = max(0, min(100, raw_to_pct(val, 'pollution_rate')))
#             elif 'hpi' in name or 'price' in name:
#                 st.session_state['hpi'] = max(0, min(100, raw_to_pct(val, 'hpi_weight')))

#     except:
#         st.warning(f"Could not load stats for {selected_country}. Using defaults.")


# st.divider()

# ── Raw range conversion (put this BEFORE the country select) ─────────────────
# run this once to populate the social_indicator_stats table

RAW_RANGES = {
    'crime_rate':     (0.0,  37.3),
    'noise_rate':     (3.2,  55.9),
    'pollution_rate': (1.6,  43.1),
    'hpi_weight':     (-9.1, 14.3),
}

def pct_to_raw(pct, col):
    low, high = RAW_RANGES[col]
    return low + (pct / 100) * (high - low)

def raw_to_pct(val, col):
    low, high = RAW_RANGES[col]
    return int(max(0, min(100, ((val - low) / (high - low)) * 100)))

# country change
def on_country_change():
    country = st.session_state['country_select']
    if country == "— None —":
        st.session_state['crime']     = 25
        st.session_state['noise']     = 25
        st.session_state['pollution'] = 25
        st.session_state['hpi']       = 40
        return
    try:
        stats_resp = requests.get(
            "http://web-api:4000/housing/social-indicator-stats",
            params={"country": country}
        )
        stats_resp.raise_for_status()
        stats = stats_resp.json()

        # group by indicator, take most recent year
        latest = {}
        for s in stats:
            name = s.get('name', '').lower()
            year = int(s.get('year', 0))
            val  = float(s.get('value', 0))  # cast string to float
            if name not in latest or year > latest[name]['year']:
                latest[name] = {'year': year, 'value': val}

        for name, data in latest.items():
            val = data['value']
            if 'crime' in name:
                st.session_state['crime'] = raw_to_pct(val, 'crime_rate')
            elif 'noise' in name:
                st.session_state['noise'] = raw_to_pct(val, 'noise_rate')
            elif 'pollution' in name:
                st.session_state['pollution'] = raw_to_pct(val, 'pollution_rate')
            elif 'hpi' in name or 'price' in name:
                st.session_state['hpi'] = raw_to_pct(val, 'hpi_weight')

    except Exception as e:
        st.write(f"Error: {e}")

# ── Country select ────────────────────────────────────────────────────────────

st.subheader("Start from a country")

try:
    countries_resp = requests.get("http://web-api:4000/housing/country")
    countries_resp.raise_for_status()
    country_list = [c['country_name'] for c in countries_resp.json()]
except:
    country_list = []

st.selectbox(
    "Select a country to pre-fill with real values",
    options=["— None —"] + sorted(country_list),
    key="country_select",
    on_change=on_country_change,   # this fires BEFORE next rerun
)

st.divider()

# ── Sliders (key must match session_state keys set in callback) ───────────────

st.subheader("Environmental conditions")

col1, col2 = st.columns(2)

with col1:
    crime     = st.slider("🔒 Crime Levels",  0, 100, 25, key="crime")
    pollution = st.slider("🌫️ Pollution Levels",  0, 100, 25, key="pollution")

with col2:
    noise = st.slider("🔊 Noise Levels",          0, 100, 25, key="noise")
    hpi   = st.slider("🏠 Housing Price Growth",  0, 100, 40, key="hpi")

st.subheader("Area type")
 
urb = st.radio(
    "",
    options=["Cities", "Towns & Suburbs", "Rural Areas"],
    horizontal=True,
    label_visibility="collapsed"
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


if st.button("Predict", type="primary", use_container_width=True):
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

        if score_display >= 8.0:
            note = "These conditions are associated with high life satisfaction!"
        elif score_display >= 7.0:
            note = "A reasonable quality of life is expected."
        elif score_display >= 6.0:
            note = "Some friction in daily life is likely."
        else:
            note = "These conditions are associated with lower wellbeing."

        st.markdown(f"""
            <div style="
                border-radius: 12px;
                padding: 28px 32px;
                text-align: center;
                margin-top: 12px;
            ">
                <p style="font-size: 0.85rem; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em;">
                    Predicted Life Satisfaction Score
                </p>
                <p style="font-size: 3.5rem; font-weight: 600; color: #1a1a2e; margin: 0; line-height: 1.1;">
                    {score_display} <span style="font-size: 1.5rem; color: #999;">/ 10</span>
                </p>
                <p style="font-size: 0.9rem; color: #444; margin-top: 16px;">
                    {note}
                </p>
            </div>
        """, unsafe_allow_html=True)

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend. Make sure the Flask server is running on port 4000.")
    except Exception as e:
        st.error(f"Something went wrong: {e}")

        