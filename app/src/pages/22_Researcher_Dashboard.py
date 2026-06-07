import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

css = """
.st-key-bg_container_1,
.st-key-bg_container_2,
.st-key-bg_container_3,
.st-key-bg_container_4 {
    background-color: rgba(185, 188, 189, 0.3);
}
"""

st.html(f"<style>{css}</style>")

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Reseacher Dashboard")

API_BASE = "http://web-api:4000"

square1, square2, square3, square4 = st.columns(4)

with square1:
    with st.container(key="bg_container_1"):
        st.subheader("Total Amount:")
        try:
            response = requests.get(f"{API_BASE}/user_growing/count", timeout=5)
            response.raise_for_status()
            total_count = response.json().get("count", 0)
            st.write(total_count)
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to load crop distribution: {e}")
        
with square2:
    with st.container(key="bg_container_2"):
        st.subheader("something")
        st.write("Bleh")
        
with square3:
    with st.container(key="bg_container_3"):
        st.subheader("Average Growth")
        st.write("Bleh")
        
with square4:
    with st.container(key="bg_container_4"):
        st.subheader("something else")
        st.write("Bleh")


crop_distrib, comparison = st.columns([3, 2])
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
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load crop distribution: {e}")

community, water, something = st.columns(3)
