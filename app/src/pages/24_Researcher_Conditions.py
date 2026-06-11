import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Explore Crop Conditions")
st.write("Query and filter crop observations across farms.")

CROPS = ['vegetables', 'bulbvegetables', 'colecrops', 'Root&tuber',
         'fibre crop', 'oil seeds', 'pulses', 'millets', 'cereals', 'sugar crops']
SEASONS = ['Monsoon (Kharif)', 'Winter (Rabi)', 'Summer (Zaid)']
WATER = ['rainfed', 'irrigated']

try:
    response = requests.get(f"{API_BASE}/user_growing/", timeout=5)
    df = pd.DataFrame(response.json())
except:
    st.error("Could not load data")
    st.stop()

try:
    map_response = requests.get(f"{API_BASE}/user_growing/map-data", timeout=5)
    map_df = pd.DataFrame(map_response.json())
except:
    map_df = pd.DataFrame()

col1, col2, col3 = st.columns(3)
with col1:
    crop_filter = st.selectbox("Crop", ["All"] + CROPS)
with col2:
    season_filter = st.selectbox("Season", ["All"] + SEASONS)
with col3:
    water_filter = st.selectbox("Water source", ["All"] + WATER)

st.divider()

filtered = df.copy()
if crop_filter != "All":
    filtered = filtered[filtered['type_of_crop'] == crop_filter]
if season_filter != "All":
    filtered = filtered[filtered['season'] == season_filter]
if water_filter != "All":
    filtered = filtered[filtered['water_source'] == water_filter]

st.write(f"**{len(filtered)} observations** match your filters")

st.dataframe(
    filtered[['farm_id', 'type_of_crop', 'season', 'sown',
              'harvested', 'water_source', 'temp', 'relative_humidity']],
    use_container_width=True
)

st.divider()

st.subheader("Inspect a farm")

if not map_df.empty:
    selected_farm_id = st.selectbox(
        "Select a farm",
        options=map_df["farm_id"].tolist(),
        format_func=lambda fid: (
            f"Farm #{fid} — "
            f"{map_df.loc[map_df['farm_id'] == fid, 'farm_name'].iloc[0]}"
        ),
        index=None,
        placeholder="Select a farm to see its growing history…",
    )

    if selected_farm_id:
        try:
            r = requests.get(f"{API_BASE}/user_growing/farm/{selected_farm_id}", timeout=5)
            history = pd.DataFrame(r.json())
        except:
            st.warning("No growing history found for this farm.")
            history = pd.DataFrame()

        farm_row = map_df[map_df["farm_id"] == selected_farm_id].iloc[0]
        st.subheader(f"Farm #{selected_farm_id} — {farm_row['farm_name']}")
        st.caption(
            f"{farm_row['country']} · "
            f"{float(farm_row['latitude']):.2f}°N, {float(farm_row['longitude']):.2f}°E"
        )

        if not history.empty:
            history = history.drop(columns=['duration_days'], errors='ignore')
            st.dataframe(
                history,
                column_config={
                    "type_of_crop":      st.column_config.TextColumn("Crop"),
                    "season":            st.column_config.TextColumn("Season"),
                    "sown":              st.column_config.TextColumn("Sown"),
                    "harvested":         st.column_config.TextColumn("Harvested"),
                    "water_source":      st.column_config.TextColumn("Water"),
                    "temp":              st.column_config.NumberColumn("Temp °C", format="%.1f"),
                    "relative_humidity": st.column_config.NumberColumn("Humidity %", format="%.1f"),
                },
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info("This farm has no growing records yet.")
else:
    st.info("No farm data available.")