import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import numpy as np
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Regional Overview Map")
st.write("Policy makers can view regional farming suitability, crop data, and environmental risk factors.")

col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    region_search = st.text_input("Search Region")

with col2:
    time_period = st.selectbox("Time Period", ["2024", "2023", "2022", "Last 5 Years"])

with col3:
    data_layer = st.selectbox(
        "Data Layer",
        ["Overall Suitability", "Soil Quality", "Flood Risk", "Crop Type", "Crop Price"]
    )

region_data = pd.DataFrame({
    "Region": ["North Valley", "East Farms", "South Plains", "River District", "West Hills"],
    "Suitability": ["High", "Low", "Moderate", "Very High", "Low"],
    "Main Crop": ["Wheat", "Corn", "Soybeans", "Rice", "Wheat"],
    "Productivity": [87, 62, 74, 91, 58],
    "Crop Price": [6.40, 5.20, 4.80, 7.10, 5.90],
    "Soil Quality": [82, 55, 70, 90, 49],
    "Flood Risk": ["Low", "High", "Moderate", "Low", "High"],
    "lat": [50.879, 50.860, 50.850, 50.890, 50.840],
    "lon": [4.700, 4.720, 4.680, 4.740, 4.660]
})

st.divider()

left_col, map_col = st.columns([1, 3])

with left_col:
    st.subheader("Key")
    st.write("Very High")
    st.write("High")
    st.write("Moderate")
    st.write("Low")
    st.write("Very Low")

    st.subheader("Other Info")
    st.write("- Soil Quality")
    st.write("- Flood Risk")
    st.write("- Main Crop Type")
    st.write("- Average Crop Price")

with map_col:
    st.subheader("Map View")
    st.map(region_data, latitude="lat", longitude="lon", zoom=10)

selected_region = st.selectbox("Select District", region_data["Region"])
selected = region_data[region_data["Region"] == selected_region].iloc[0]

st.divider()

st.subheader(f"{selected['Region']} — {selected['Suitability']} Suitability")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Main Crop Type", selected["Main Crop"])
col2.metric("Average Productivity", f"{selected['Productivity']}%")
col3.metric("Average Crop Price", f"${selected['Crop Price']}")
col4.metric("Soil Quality", f"{selected['Soil Quality']}/100")

col1, col2 = st.columns(2)

with col1:
    if st.button("Save Analysis"):
        st.success("Analysis saved!")

with col2:
    if st.button("Generate Report"):
        st.info("Report generation coming soon.")
