import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Add Farm Information")
st.write("Use the tabs below to register a new farm, set its location, and log a growing record.")

tab1, tab2, tab3 = st.tabs(["🌾 Farm", "📍 Location", "🌱 Growing Record"])


# ─────────────────────────────────────────────
# TAB 1 — Create a farm (POST /farms/farms)
# Creates both a farms row AND a farms_location row in one request
# ─────────────────────────────────────────────
with tab1:
    st.subheader("Register a new farm")
    st.caption("This will create the farm and its location together.")

    with st.form("farm_form"):
        col1, col2 = st.columns(2)

        with col1:
            farm_name  = st.text_input("Farm name *", placeholder="e.g. Sunshine Farm")
            user_id    = st.number_input("Your user ID *", min_value=1, step=1)

        with col2:
            country   = st.text_input("Country *", placeholder="e.g. Spain")
            latitude  = st.number_input("Latitude *",  min_value=-90.0,  max_value=90.0,  value=20.5, format="%.6f")
            longitude = st.number_input("Longitude *", min_value=-180.0, max_value=180.0, value=78.9, format="%.6f")

        submitted = st.form_submit_button("Register farm", use_container_width=True, type="primary")

    if submitted:
        missing = []
        if not farm_name:  missing.append("Farm name")
        if not country:    missing.append("Country")

        if missing:
            st.error(f"Please fill in: {', '.join(missing)}")
        else:
            payload = {
                "farm_name":  farm_name,
                "user_id":    int(user_id),
                "created_by": int(user_id),
                "longitude":  longitude,
                "latitude":   latitude,
                "country":    country,
            }
            try:
                r = requests.post(f"{API_BASE}/farms/farms", json=payload)
                if r.status_code == 201:
                    data = r.json()
                    st.success(f"Farm registered! Farm ID: **{data['farm_id']}** — note this for adding growing records.")
                else:
                    st.error(f"Error {r.status_code}: {r.json().get('error', 'Unknown error')}")
            except requests.ConnectionError:
                st.error("Could not reach the API. Is the backend running?")


# ─────────────────────────────────────────────
# TAB 2 — Add/update a farm location (POST /farm_loc/)
# Use this if the farm already exists but has no location,
# or to add a second location entry
# ─────────────────────────────────────────────
with tab2:
    st.subheader("Add a location to an existing farm")
    st.caption("Use this if you already have a farm ID but need to set or update its location separately.")

    with st.form("loc_form"):
        col1, col2 = st.columns(2)

        with col1:
            loc_farm_id   = st.number_input("Farm ID *", min_value=1, step=1, key="loc_farm_id")
            loc_country   = st.text_input("Country *", placeholder="e.g. Belgium", key="loc_country")

        with col2:
            loc_latitude  = st.number_input("Latitude *",  min_value=-90.0,  max_value=90.0,  value=20.5, format="%.6f", key="loc_lat")
            loc_longitude = st.number_input("Longitude *", min_value=-180.0, max_value=180.0, value=78.9, format="%.6f", key="loc_lon")

        loc_submitted = st.form_submit_button("Save location", use_container_width=True, type="primary")

    if loc_submitted:
        missing = []
        if not loc_country:    missing.append("Country")

        if missing:
            st.error(f"Please fill in: {', '.join(missing)}")
        else:
            payload = {
                "farm_id":    int(loc_farm_id),
                "longitude":  loc_longitude,
                "latitude":   loc_latitude,
                "country":    loc_country,
                "created_by": "mock",
            }
            try:
                r = requests.post(f"{API_BASE}/farm_loc/", json=payload)
                if r.status_code == 201:
                    st.success(f"Location saved for Farm ID {int(loc_farm_id)}.")
                else:
                    st.error(f"Error {r.status_code}: {r.json().get('error', 'Unknown error')}")
            except requests.ConnectionError:
                st.error("Could not reach the API. Is the backend running?")


# ─────────────────────────────────────────────
# TAB 3 — Log a growing record (POST /user_growing/)
# Maps to user_growing_data: crop, season, conditions, NPK
# ─────────────────────────────────────────────
with tab3:
    st.subheader("Log a growing record")
    st.caption("Record the conditions and crop details for one growing cycle on your farm.")

    with st.form("growing_form"):

        # Identifiers
        col1, col2 = st.columns(2)
        with col1:
            g_farm_id    = st.number_input("Farm ID *", min_value=1, step=1, key="g_farm_id")
        with col2:
            g_crop = st.selectbox("Crop type *", [
                "Cereals", "Vegetables", "Pulses", "Oil seeds",
                "Sugar crops", "Millets", "Root & tuber", "Fibre crop",
            ])
            g_season = st.selectbox("Season *", ["Kharif", "Rabi", "Zaid"])

        st.divider()

        # Timing
        st.markdown("**Timing**")
        col3, col4 = st.columns(2)
        with col3:
            g_sown      = st.selectbox("Month sown *", [
                "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"
            ], index=5)
        with col4:
            g_harvested = st.selectbox("Month harvested *", [
                "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"
            ], index=10)

        st.divider()

        # Growing conditions
        st.markdown("**Growing conditions**")
        col5, col6, col7 = st.columns(3)
        with col5:
            g_water = st.selectbox("Water source *", ["Irrigated", "Rainfed"])
            g_temp  = st.number_input("Temperature (°C) *", min_value=-10.0, max_value=55.0, value=25.0, format="%.1f")
        with col6:
            g_humidity = st.number_input("Relative humidity (%) *", min_value=0.0, max_value=100.0, value=65.0, format="%.1f")
        with col7:
            st.markdown(" ")  # spacer

        st.divider()

        # NPK values
        st.markdown("**Soil nutrients (NPK)**")
        st.caption("Nitrogen (N), Phosphorus (P), Potassium (K) — used by the crop recommendation model.")
        col8, col9, col10 = st.columns(3)
        with col8:
            g_n = st.number_input("N (kg/ha) *", min_value=0.0, max_value=500.0, value=90.0, format="%.1f")
        with col9:
            g_p = st.number_input("P (kg/ha) *", min_value=0.0, max_value=500.0, value=42.0, format="%.1f")
        with col10:
            g_k = st.number_input("K (kg/ha) *", min_value=0.0, max_value=500.0, value=43.0, format="%.1f")

        g_submitted = st.form_submit_button("Log growing record", use_container_width=True, type="primary")

    if g_submitted:
        payload = {
            "farm_id":           int(g_farm_id),
            "n":                 g_n,
            "p":                 g_p,
            "k":                 g_k,
            "type_of_crop":      g_crop,
            "season":            g_season,
            "sown":              g_sown,
            "harvested":         g_harvested,
            "water_source":      g_water.lower(),   # schema stores 'irrigated'/'rainfed'
            "temp":              g_temp,
            "relative_humidity": g_humidity,
            "created_by":        "mock",
        }
        try:
            r = requests.post(f"{API_BASE}/user_growing/", json=payload)
            if r.status_code == 201:
                data = r.json()
                st.success(f"Growing record logged! Record ID: **{data['user_growing_data_id']}**")
                st.info("This data will be used to improve crop recommendations for all farmers.")
            else:
                st.error(f"Error {r.status_code}: {r.json().get('error', 'Unknown error')}")
        except requests.ConnectionError:
            st.error("Could not reach the API. Is the backend running?")