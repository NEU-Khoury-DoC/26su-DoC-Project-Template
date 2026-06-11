import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
import altair as alt
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
SideBarLinks()

st.title("Researcher Dashboard")
st.write('General overview of collected crop information')

API_BASE = "http://web-api:4000"

try:
    response = requests.get(f"{API_BASE}/user_growing/stats", timeout=5)
    response.raise_for_status()
    stats = response.json()
    total_count = stats.get('total_observations', '—')
    distinct = stats.get('crop_types', '—')
    total_farms = stats.get('total_farms', '—')
except:
    total_count = avg_growth = distinct = total_farms = '—'

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='stat-card'><h3>Total Observations</h3><p>{total_count}</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='stat-card'><h3>Distinct Crops</h3><p>{distinct}</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='stat-card'><h3>Total Farms</h3><p>{total_farms}</p></div>", unsafe_allow_html=True)

st.divider()

CHART_HEIGHT = 400  # single source of truth — both columns match this

crop_distrib, side_panel = st.columns([3, 1])

with crop_distrib:
    st.subheader("Crop distribution")
    try:
        response = requests.get(f"{API_BASE}/user_growing/count-by-crop", timeout=5)
        response.raise_for_status()
        crop_counts = response.json()

        if crop_counts:
            chart_data_crop = pd.DataFrame(crop_counts)
            chart_data_crop = chart_data_crop.rename(columns={"type_of_crop": "Crop", "count": "Count"})
            crop_chart = (
                alt.Chart(chart_data_crop)
                .mark_bar()
                .encode(
                    x=alt.X("Crop:N", sort="-y"),
                    y=alt.Y("Count:Q"),
                    tooltip=["Crop", "Count"],
                )
                .properties(height=CHART_HEIGHT)
            )
            st.altair_chart(crop_chart, use_container_width=True)
        else:
            st.info("No crop observations found yet.")
    except:
        st.error("Failed to load crop distribution")

with side_panel:
    st.subheader("By farm")
    try:
        response = requests.get(f"{API_BASE}/user_growing/count-by-farm", timeout=5)
        response.raise_for_status()
        farm_counts = response.json()

        if farm_counts:
            chart_data_farm = pd.DataFrame(farm_counts)
            chart_data_farm = chart_data_farm.rename(columns={"farm_id": "Farm", "count": "Count"})
            chart_data_farm["Farm"] = chart_data_farm["Farm"].astype(str)

            # Make the chart tall enough to show all farms, then clip it to
            # CHART_HEIGHT so the column scrolls rather than overflows the page
            bar_height = 24
            full_height = max(len(chart_data_farm) * bar_height, CHART_HEIGHT)

            farm_chart = (
                alt.Chart(chart_data_farm)
                .mark_bar()
                .encode(
                    y=alt.Y("Farm:N", sort="-x", axis=alt.Axis(labelLimit=60)),
                    x=alt.X("Count:Q"),
                    tooltip=["Farm", "Count"],
                )
                .properties(height=full_height)
            )
            st.altair_chart(farm_chart, use_container_width=True)
        else:
            st.info("No farm observations found yet.")
    except:
        st.error("Failed to load farm distribution")