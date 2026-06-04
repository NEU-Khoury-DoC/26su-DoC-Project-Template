import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
import folium
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from streamlit_folium import st_folium
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Risk Heatmap")
st.caption("Visualize social indicator risk levels across EU countries.")

GEOJSON_URL = "https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson"

#filters
indicator_types = st.multiselect(
    "Shade By Indicator",
    ["Pollution", "Crime, Violence, and Vandalism", "Poverty",
     "Overcrowding", "Noise", "House Price Index"],
    default=["Poverty"]
)

selected_year = st.selectbox(
    "Year",
    [str(y) for y in range(2010, 2026)],
    index=len(range(2010, 2026)) - 1
)

#getting and aggregating data 
try:
    if not indicator_types:
        st.info("Select at least one indicator.")
    else:
        all_data = []
        for ind in indicator_types:
            r = requests.get(
                "http://web-api:4000/housing/social-indicator-stats",
                params={"social_indicator_type": ind, "year": selected_year}
            )
            if r.status_code == 200 and r.json():
                df_temp = pd.DataFrame(r.json())[["country_name", "value"]]
                df_temp["value"] = pd.to_numeric(df_temp["value"], errors="coerce")
                all_data.append(df_temp)

        if all_data:
            df = pd.concat(all_data).groupby("country_name")["value"].mean().reset_index()
            df = df.dropna().sort_values("value", ascending=False).reset_index(drop=True)

            # Color map
            cmap = plt.get_cmap('RdYlGn_r')
            norm = mcolors.Normalize(vmin=df["value"].min(), vmax=df["value"].max())

            def get_color(value):
                return mcolors.to_hex(cmap(norm(value)))

            # Build color lookup
            color_map = {row["country_name"]: get_color(row["value"]) for _, row in df.iterrows()}
            value_map = {row["country_name"]: row["value"] for _, row in df.iterrows()}

            # ── Map ───────────────────────────────────────────────────────────
            geo_data = requests.get(GEOJSON_URL).json()

            m = folium.Map(location=[54.5260, 15.2551], zoom_start=4)

            folium.GeoJson(
                geo_data,
                style_function=lambda feature: {
                    'fillColor': color_map.get(feature['properties'].get('NAME', ''), '#cccccc'),
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7,
                },
                tooltip=folium.GeoJsonTooltip(
                    fields=['NAME'],
                    aliases=['Country'],
                    localize=True
                ),
                popup=folium.GeoJsonPopup(
                    fields=['NAME'],
                    aliases=['Country'],
                )
            ).add_to(m)

            st_folium(m, width=1250, height=500, returned_objects=[])

            st.caption("Map boundaries: leakyMirror/map-of-europe (GitHub), MIT License.")

        else:
            st.info("No data — sync indicators first via the Plan Funds page.")

except Exception as e:
    st.error(f"Error: {e}")