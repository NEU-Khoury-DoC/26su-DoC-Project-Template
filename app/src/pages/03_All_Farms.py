import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("All Farms")
st.write("Browse all farms currently registered in the database.")

# API
API_URL = "http://web-api:4000/farms/farms"

try:
    response = requests.get(API_URL, timeout=5)

    if response.status_code == 200:
        farms = response.json()

        if not farms:
            st.info("No farms found in the database yet.")
        else:
            #country filter
            countries = sorted({f["country"] for f in farms if f.get("country")})
            selected_country = st.selectbox("Filter by Country", ["All"] + countries)

            if selected_country != "All":
                farms = [f for f in farms if f.get("country") == selected_country]

            st.write(f"Found {len(farms)} farms")

            df = pd.DataFrame(farms)
            display_cols = ["farm_id", "farm_name", "owner_name", "country", "latitude", "longitude"]
            display_cols = [c for c in display_cols if c in df.columns]

            st.dataframe(
                df[display_cols].rename(columns={
                    "farm_id": "ID",
                    "farm_name": "Farm Name",
                    "owner_name": "Owner",
                    "country": "Country",
                    "latitude": "Latitude",
                    "longitude": "Longitude",
                }),
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.error(f"Failed to fetch farm data from the API (status {response.status_code}).")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
