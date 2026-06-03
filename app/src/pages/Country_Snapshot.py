import logging
logger = logging.getLogger(__name__)

import altair as alt
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Country Snapshot")
st.write("#### All indicators in one place")

COUNTRIES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus",
    "Czech Republic", "Denmark", "Estonia", "Finland", "France",
    "Germany", "Greece", "Hungary", "Ireland", "Italy",
    "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
    "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
    "Spain", "Sweden",
]

# Persist country selection so the other journalist pages can read it.
default_country = st.session_state.get("journalist_country", "Poland")
selected_country = st.selectbox(
    "Select Country",
    COUNTRIES,
    index=COUNTRIES.index(default_country) if default_country in COUNTRIES else 0,
)
st.session_state["journalist_country"] = selected_country

st.divider()

# Country header
st.subheader(selected_country)
st.caption("Latest reported values · placeholder data")

# Headline indicators
m1, m2, m3, m4 = st.columns(4)
m1.metric("Electricity Price", "€000/MWh", "+0% WoW")
m2.metric("Gas Storage", "00%", "-0pp MoM")
m3.metric("Renewables Share", "00%", "+0pp YoY")
m4.metric("Import Dependence", "00%", "-0pp YoY")

st.divider()

# Where the country's electricity comes from
st.write("##### Where the electricity comes from")
# Placeholder shares (sum to 100) so the chart renders until real data is wired in.
mix_df = pd.DataFrame(
    {
        "Source": ["Nuclear", "Gas", "Coal", "Wind", "Solar", "Hydro", "Other"],
        "Share (%)": [20, 20, 15, 15, 10, 10, 10],
    }
)
mix_chart = (
    alt.Chart(mix_df)
    .mark_bar()
    .encode(
        # Lock the value axis to 0–100 so it never shows negative numbers.
        x=alt.X("Share (%):Q", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Source:N", sort=None, title=None),
    )
)
st.altair_chart(mix_chart, use_container_width=True)

st.divider()

# Cross-page navigation
nav_left, nav_right = st.columns(2)
with nav_left:
    if st.button("View Historical Trends →", type='primary', use_container_width=True):
        st.switch_page('pages/Historical_Trends.py')
with nav_right:
    if st.button("Open Article Analysis →", type='primary', use_container_width=True):
        st.switch_page('pages/Article_Analysis.py')
