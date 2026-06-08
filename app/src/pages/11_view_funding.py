import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
import plotly.express as px

st.set_page_config(layout = 'wide')
SideBarLinks()

if st.session_state.get("scroll_to_draft"):
    st.session_state["scroll_to_draft"] = False
    st.info("Scroll down to the Draft Funding Plan section to submit your proposal.")

# running POST request to sync data from Eurostat
st.title("Explore Funding Programs")

# Funding Index Table
st.subheader("Funding Index")
st.caption("Explore existing housing and social funding programs across EU countries.")
try:
    countries_res = requests.get("http://web-api:4000/housing/country")
    countries = ["All"] + [c["country_name"] for c in countries_res.json()]

    selected_country = st.selectbox("Filter by Country", countries, key = "funding_country")

    params = {}
    if selected_country != "All":
        params["country"] = selected_country

    response = requests.get("http://web-api:4000/housing/funding", params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            agencies = ["All"] + sorted(list(set(f["agency"] for f in data if "agency" in f)))
            selected_agency = st.selectbox("Filter by Agency", agencies, key = "funding_agency")

            df = pd.DataFrame(data)[["country_name", "agency", "program", "amount", "year"]]
            df.columns = ["Country", "Agency", "Program", "Amount (€)", "Year"]

            if selected_agency != "All":
                df = df[df["Agency"] == selected_agency]

            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No funding data.")
    else:
        st.error("Could not load funding data.")
except Exception as e:
    st.error(f"Error: {e}")

st.divider()

#Draft funding plan form
st.subheader("Draft Funding Plan")

with st.container(border=True):
    program = st.text_input("Program Name")
    
    countries_res2 = requests.get("http://web-api:4000/housing/country")
    country_list = countries_res2.json() if countries_res2.status_code == 200 else []
    country_options = {c["country_name"]: c["country_id"] for c in country_list}
    selected_plan_country = st.selectbox("Country", list(country_options.keys()), key="plan_country")
    
    amount = st.number_input("Amount (€)", min_value=0, step=1000)
    
    indicators_targeted = st.multiselect(
        "Indicators Targeted",
        ["All Indicators", "Pollution", "Crime",
         "Poverty", "Overcrowding", "Noise", "House Price Index", "Under-occupied"],
        default=["All Indicators"]
    )
    demographics_targeted = st.multiselect(
        "Demographics Targeted",
        ["All Demographics", "Students", "Low Income", "Elderly", "Families"],
        default=["All Demographics"]
    )
    
    description = st.text_area("Description")
    
    if st.button("Submit Draft", type="primary"):
        if not program or not description:
            st.warning("Please fill in Program Name and Description.")
        else:
            try:
                payload = {
                    "user_id": st.session_state.get("user_id", 1),
                    "country_id": country_options[selected_plan_country],
                    "program": program,
                    "amount": amount,
                    "indicators_targeted": ", ".join(indicators_targeted),
                    "demographics_targeted": ", ".join(demographics_targeted),
                    "description": description
                }
                response = requests.post("http://web-api:4000/housing/funding-draft", json=payload)
                if response.status_code == 201:
                    st.success("Draft saved successfully!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")

#Button for funding drafts page
if st.button("View My Funding Drafts", type = "secondary"):
    st.switch_page("pages/13_funding_drafts.py")