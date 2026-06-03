import logging
logger = logging.getLogger(__name__)

import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Historical Trends")
st.write("#### Same date, prior years")
st.caption("Placeholder data — indicators map to Eurostat / Ember / AGSI once wired in.")

COUNTRIES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus",
    "Czech Republic", "Denmark", "Estonia", "Finland", "France",
    "Germany", "Greece", "Hungary", "Ireland", "Italy",
    "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
    "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
    "Spain", "Sweden",
]

INDICATORS = [
    "Electricity Price (€/MWh)",
    "Gas Storage (%)",
    "Import Dependence (%)",
    "Renewables Share (%)",
    "Carbon Intensity (gCO₂/kWh)",
]

# Filter row
filter_left, filter_mid, filter_right = st.columns([2, 2, 1])

with filter_left:
    default_country = st.session_state.get("journalist_country", "Poland")
    selected_country = st.selectbox(
        "Country",
        COUNTRIES,
        index=COUNTRIES.index(default_country) if default_country in COUNTRIES else 0,
    )
    st.session_state["journalist_country"] = selected_country

with filter_mid:
    indicator = st.selectbox("Indicator", INDICATORS)

with filter_right:
    year_range = st.slider("Years", min_value=2015, max_value=2025, value=(2021, 2025))

st.divider()

# Placeholder multi-year dataset (one column per indicator).
all_years = list(range(2015, 2026))
all_data = pd.DataFrame(
    {name: [0] * len(all_years) for name in INDICATORS},
    index=[str(y) for y in all_years],
)

mask = [year_range[0] <= int(y) <= year_range[1] for y in all_data.index]
trimmed = all_data[mask]

# Single-indicator trend
st.write(f"### {indicator} — {selected_country}")
st.line_chart(trimmed[[indicator]])

st.divider()

# Cross-page navigation
nav_left, nav_right = st.columns(2)
with nav_left:
    if st.button("← Back to Country Snapshot", use_container_width=True):
        st.switch_page('pages/Country_Snapshot.py')
with nav_right:
    if st.button("Open Article Analysis →", type='primary', use_container_width=True):
        st.switch_page('pages/Article_Analysis.py')
