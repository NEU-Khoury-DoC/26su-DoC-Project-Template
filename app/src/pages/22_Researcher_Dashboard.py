import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

css = """
<style>
.stat-card {
  color: black;
  padding: 18px;
  border-radius: 12px;
  text-align: center;
  font-family: 'Courier New', monospace;
}
.stat-card h3 { margin: 6px 0 8px 0; font-weight: 600; }
.stat-card p { font-size: 20px; margin: 0; }
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title("Researcher Dashboard")
st.write('Overview of collected soil/crop observations and quick actions.')

API_BASE = "http://web-api:4000"

# Top stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    try:
        response = requests.get(f"{API_BASE}/user_growing/count", timeout=5)
        response.raise_for_status()
        total_count = response.json().get("count", 0)
    except requests.exceptions.RequestException:
        total_count = '—'
    st.markdown(f"<div class='stat-card'><h3>Total Observations</h3><p>{total_count}</p></div>", unsafe_allow_html=True)

with col2:
    try:
        response = requests.get(f"{API_BASE}/user_growing/average-growth", timeout=5)
        response.raise_for_status()
        avg_growth = response.json().get('avg', '—')
    except requests.exceptions.RequestException:
        avg_growth = '—'
    st.markdown(f"<div class='stat-card'><h3>Average Growth</h3><p>{avg_growth}</p></div>", unsafe_allow_html=True)

with col3:
    try:
        response = requests.get(f"{API_BASE}/user_growing/distinct-crops", timeout=5)
        response.raise_for_status()
        distinct = response.json().get('distinct', '—')
    except requests.exceptions.RequestException:
        distinct = '—'
    st.markdown(f"<div class='stat-card'><h3>Distinct Crops</h3><p>{distinct}</p></div>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<div class='stat-card'><h3>New This Week</h3><p>—</p></div>", unsafe_allow_html=True)

# Main content: distribution and quick compare
crop_distrib, side_panel = st.columns([3, 1])

with crop_distrib:
    st.subheader("Crop distribution")
    try:
        response = requests.get(f"{API_BASE}/user_growing/count-by-crop", timeout=5)
        response.raise_for_status()
        crop_counts = response.json()

        if crop_counts:
            chart_data = pd.DataFrame(crop_counts)
            chart_data = chart_data.rename(columns={"type_of_crop": "Crop", "count": "Count"})
            st.bar_chart(chart_data.set_index("Crop")["Count"], use_container_width=True)
        else:
            st.info("No crop observations found yet.")
    except requests.exceptions.RequestException:
        st.error("Failed to load crop distribution")

with side_panel:
    st.subheader('Quick Compare')
    region_a = st.selectbox('Region A', ['North Valley', 'East Farms', 'South Plains'])
    region_b = st.selectbox('Region B', ['River District', 'West Hills', 'North Valley'])
    if st.button('Run Quick Compare'):
        st.write(f'Placeholder comparison for {region_a} vs {region_b}')

st.markdown('---')

community, water, misc = st.columns(3)

with community:
    st.subheader('Community Reports')
    st.write('Recent reports and flags will appear here.')

with water:
    st.subheader('Water Index')
    st.write('Placeholder for water/irrigation indicators')

with misc:
    st.subheader('Notes')
    st.write('Quick links and actions')
