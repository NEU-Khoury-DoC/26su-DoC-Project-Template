import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"


# ── Data fetching via REST API ───────────────────────────────────
@st.cache_data(ttl=300)
def load_map_data(season: str) -> pd.DataFrame:
    params = {}
    if season != "All":
        params["season"] = season
    r = requests.get(f"{API_BASE}/user_growing/map-data", params=params)
    r.raise_for_status()
    return pd.DataFrame(r.json())


@st.cache_data(ttl=300)
def load_farm_history(farm_id: int) -> pd.DataFrame:
    r = requests.get(f"{API_BASE}/user_growing/farm/{farm_id}")
    r.raise_for_status()
    return pd.DataFrame(r.json())


# ── Color mapping ────────────────────────────────────────────────
CROP_COLORS = {
    "Cereals":      [29,  158, 117],
    "Vegetables":   [127, 119, 221],
    "Pulses":       [216,  90,  48],
    "Oil seeds":    [186, 117,  23],
    "Sugar crops":  [55,  138, 221],
    "Millets":      [136, 135, 128],
    "Root & tuber": [212,  83, 126],
}
WATER_COLORS = {
    "Irrigated": [29, 158, 117],
    "Rainfed":   [216, 90,  48],
}

def assign_color(df: pd.DataFrame, color_by: str) -> pd.DataFrame:
    df = df.copy()
    
    def no_data(row):
        return row['record_count'] == 0 or pd.isna(row['avg_temp'])
    
    if color_by == "Crop type":
        df["color"] = df.apply(
            lambda row: [128, 128, 128] if no_data(row) else CROP_COLORS.get(row['dominant_crop'], [136, 135, 128]),
            axis=1
        )
    elif color_by == "Water source":
        df["color"] = df.apply(
            lambda row: [128, 128, 128] if no_data(row) else (WATER_COLORS["Irrigated"] if row['has_irrigated'] else WATER_COLORS["Rainfed"]),
            axis=1
        )
    else:  # Temperature
        t_min, t_max = df["avg_temp"].min(), df["avg_temp"].max()
        def temp_to_color(row):
            if no_data(row):
                return [128, 128, 128]
            norm = (row['avg_temp'] - t_min) / max(t_max - t_min, 1)
            return [
                int(133 + (216 - 133) * norm),
                int(183 - (183 - 90)  * norm),
                int(235 - (235 - 48)  * norm),
            ]
        df["color"] = df.apply(temp_to_color, axis=1)
    return df


# ── Page ─────────────────────────────────────────────────────────
st.title("Farm map")
st.caption("Each dot is one farm. Color encodes the selected dimension.")

col1, col2 = st.columns([2, 1])
with col1:
    color_by = st.segmented_control(
        "Color by",
        ["Crop type", "Water source", "Temperature"],
        default="Crop type",
    )
with col2:
    season = st.pills(
        "Season",
        ["All", "Kharif", "Rabi", "Zaid"],
        default="All",
    )

# Load data — handle empty result gracefully
try:
    df = load_map_data(season)
except requests.HTTPError as e:
    st.error(f"Could not load map data: {e}")
    st.stop()

if df.empty:
    st.info("No farm data found for the selected filters.")
    st.stop()

df = assign_color(df, color_by)

# Stats bar
c1, c2, c3, c4 = st.columns(4)
c1.metric("Farms shown",  len(df))
c2.metric("Countries",    df["country"].nunique())
c3.metric("Crop types",   df["dominant_crop"].nunique())
c4.metric("Avg temp",     f"{df['avg_temp'].mean():.1f}°C")

# Map
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["longitude", "latitude"],  # match column names from API
    get_fill_color="color",
    get_radius=15000,
    pickable=True,
    auto_highlight=True,
    highlight_color=[255, 255, 255, 80],
)

view = pdk.ViewState(
    latitude=df["latitude"].mean(),
    longitude=df["longitude"].mean(),
    zoom=3,
    pitch=0,
)

tooltip = {
    "html": (
        "<b>Farm #{farm_id} — {farm_name}</b><br/>"
        "{country}<br/>"
        "Dominant crop: {dominant_crop}<br/>"
        "Avg temp: {avg_temp}°C · Humidity: {avg_humidity}%<br/>"
        "Records: {record_count}"
    ),
    "style": {
        "backgroundColor": "white",
        "color": "#333",
        "fontSize": "12px",
        "padding": "8px",
    }
}

st.pydeck_chart(
    pdk.Deck(layers=[layer], initial_view_state=view, tooltip=tooltip),
    use_container_width=True,
    height=420,
)
