import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
import plotly.express as px

SideBarLinks()

with st.container(border=True):
    title = st.text_input("Listing Title")
    city = st.text_input('City')

    countries_res2 = requests.get("http://web-api:4000/housing/country")
    country_list = countries_res2.json() if countries_res2.status_code == 200 else []
    country_options = {c["country_name"]: c["country_id"] for c in country_list}
    selected_country = st.selectbox("Country", list(country_options.keys()), key="plan_country")

    uni_res2 = requests.get("http://web-api:4000/housing/university", params={"limit":1000})
    uni_list = uni_res2.json() if uni_res2.status_code == 200 else []
    uni_options = {c["university_name"]: c["university_id"] for c in uni_list}
    selected_uni = st.selectbox("University", list(uni_options.keys()), key="associated_uni")

    price = st.number_input("Amount (€/Month)", min_value=0, max_value=3000, step=500)

    property_type = st.selectbox('Property type', ['Townhouse', 'Studio Apartment', 'Apartment', 'House'])

    if st.button("Submit Draft", type="primary"):
        if not(title and price and property_type and city):
            st.warning("Please fill in Program Name and Description.")
        else:
            try:
                payload = {
                    "user_id": st.session_state.get("user_id", 1),
                    "title": title,
                    "country_id": country_options[selected_country],
                    "price": price,
                    "associated_university_id": uni_options[selected_uni],
                    "property_type": property_type,
                    "city_name": city
                }
                response = requests.post("http://web-api:4000/housing/listing", json=payload)
                if response.status_code == 201:
                    st.success("Draft saved successfully!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

