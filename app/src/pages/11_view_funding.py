import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
import plotly.express as px

st.set_page_config(layout = 'wide')
SideBarLinks()

# running POST request to sync data from Eurostat
st.title("Plan Funds")
if st.button("Sync Eurostat Data", type = "secondary"):
    with st.spinner("Syncing..."):
        endpoints = ["pollution", "crime", "poverty", "overcrowding", "noise", "hpi"]
        for ep in endpoints:
            requests.post(f"http://web-api:4000/housing/social-indicator-stats/{ep}")
    st.success("All data synced!")
    st.rerun()

st.subheader("Funding Index")
st.caption("Existing housing and social funding programs across EU countries.")
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


# Social Indicator Index
st.subheader("Social Indicator Index")
st.caption("Explore Eurostat data on indicators by country and year.")

try:
    indicator_types = st.multiselect(
        "Demographic Type",
        ["Pollution", "Crime", "Poverty", "Overcrowding", "Noise", "House Price Index", "Under-occupied"],
        default = [],
        key = "indicator_type"
    )
    selected_countries = st.multiselect(
        "Select Countries to Compare",
        [c for c in countries if c != "All"],
        default = [],
        key = "indicator_country"
    )
    selected_years = st.multiselect(
        "Filter by Year",
        [str(y) for y in range(2010, 2026)],
        default = [],
        key = "indicator_year"
    )

    if indicator_types and selected_years:
        results = []
        for ind in indicator_types:
            for year in selected_years:
                params2 = {"social_indicator_type": ind, "year": year}
                r = requests.get("http://web-api:4000/housing/social-indicator-stats", params = params2)
                if r.status_code == 200 and r.json():
                    df_temp = pd.DataFrame(r.json())[["country_name", "year", "value"]]
                    df_temp["indicator"] = ind
                    results.append(df_temp)

        if results:
            df2 = pd.concat(results)
            df2.columns = ["Country", "Year", "Value", "Indicator"]

            if selected_countries:
                df2 = df2[df2["Country"].isin(selected_countries)]

            df2 = df2.sort_values("Value", ascending = False)
            fig = px.bar(
                df2,
                x = "Country",
                y = "Value",
                color = "Indicator",
                barmode = "stack",
                title = "Social Indicators by Country",
            )
            fig.update_layout(xaxis_tickangle=-45, height=400, yaxis_title="Rate (%)")
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("No data — sync indicators first via the Sync button.")
    else:
        st.info("Select at least one indicator and year to view the chart.")

except Exception as e:
    st.error(f"Error: {e}")

st.divider()


# Draft Funding Plan
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
        ["All Indicators", "Pollution", "Crime, Violence, and Vandalism",
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