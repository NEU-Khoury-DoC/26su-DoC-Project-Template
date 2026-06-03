import logging
logger = logging.getLogger(__name__)

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

# Headline indicators
m1, m2 = st.columns(2)
m1.metric("Electricity Price", "€118/MWh", "+4% WoW")
m2.metric("Gas Storage", "62%", "-9pp MoM")


st.divider()

# Cross-page navigation
nav_left, nav_right = st.columns(2)
with nav_left:
    if st.button("View Historical Trends →", type='primary', use_container_width=True):
        st.switch_page('pages/Historical_Trends.py')
with nav_right:
    if st.button("Open Article Analysis →", type='primary', use_container_width=True):
        st.switch_page('pages/Article_Analysis.py')