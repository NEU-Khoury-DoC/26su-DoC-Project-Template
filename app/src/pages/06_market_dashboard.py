import logging
import streamlit as st
import requests
import pandas as pd
import folium
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from modules.nav import SideBarLinks
st.set_page_config(layout='wide')

# Initialize sidebar
SideBarLinks()

st.title("Market Dashboard")

#sync button
# if st.button("Sync Eurostat Data", type = "secondary"):
#     with st.spinner("Syncing..."):
#         for ep in ["pollution", "crime", "poverty", "overcrowding", "noise", "hpi"]:
#             requests.post(f"http://web-api:4000/housing/social-indicator-stats/{ep}")
#     st.success("All data synced!")
#     st.rer

if "synced" not in st.session_state:
    st.session_state.synced = False

if not st.session_state.synced:
    with st.spinner("Syncing..."):
        for ep in ["pollution", "crime", "poverty", "overcrowding", "noise", "hpi"]:
            requests.post(f"http://web-api:4000/housing/social-indicator-stats/{ep}")
    st.session_state.synced = True
    st.success("All data synced!")
    st.rerun()


col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.write('more info')

with col2:
    with st.container(border=True):
        st.write('more info')

with col3:
    with st.container(border=True):
        st.write('more info')



INDICATOR_UNITS = {
    "Pollution": "% of population",
    "Crime, Violence, and Vandalism": "% of population",
    "Poverty": "% of population",
    "Overcrowding": "% of population",
    "Noise": "% of population",
}


#Sorting
hpi_data = requests.get(
    "http://web-api:4000/housing/social-indicator-stats",
    params={"social_indicator_type": "House Price Index"}
).json()

hpi_countries = sorted(set(row["country_name"] for row in hpi_data))

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("House Price Index over Time")

with col2:
    hpi_data = requests.get(
        "http://web-api:4000/housing/social-indicator-stats",
        params={"social_indicator_type": "House Price Index"}
    ).json()
    hpi_countries = sorted(set(row["country_name"] for row in hpi_data))
    country_filter = st.selectbox("Country", options=hpi_countries, label_visibility="collapsed")


#HPI by year chart (horizontal)
try:
    r = requests.get(
        "http://web-api:4000/housing/social-indicator-stats",
        params = {"social_indicator_type": 'House Price Index', "country": country_filter}
    )

    if r.status_code == 200 and r.json():
        df_rank = pd.DataFrame(r.json())[["year", "value"]]
        df_rank["value"] = pd.to_numeric(df_rank["value"], errors="coerce")
        df_rank = df_rank.dropna().sort_values("year", ascending=True).reset_index(drop=True)
        
        unit = "% change from 2015 baseline"
        df_rank["value"] = df_rank["value"] - 100
        df_rank.columns = ["Year", f"Value ({unit})"]

        x_label = "% Change from 2015 Baseline"
        color_scale = "ylorrd"
        range_color = [-50, 150]

        df_rank["Year"] = df_rank["Year"].astype(str)

        fig = px.bar(
            df_rank,
            x = "Year",
            y = "Value (% change from 2015 baseline)",
            orientation = 'v',
            color = "Value (% change from 2015 baseline)",
            color_continuous_scale = color_scale,
            range_color = range_color,
            labels = {"Value (% change from 2015 baseline)": x_label}
        )

        fig.update_layout(
            yaxis = dict(autorange = True),  # fix inverted y axis
            coloraxis_showscale = False,
            height = 600,
        )
        st.plotly_chart(fig, use_container_width = True)

    else:
        st.info("No data")

except Exception as e:
    st.error(f"Error loading rankings: {e}")

st.divider()

#sorting for bar chart
col11, col22 = st.columns(2)
with col11:
    selected_year = st.selectbox(
        "Year",
        [str(y) for y in range(2010, 2026)],
        index = len(range(2010, 2026)) - 1
    )

with col22:
    indicator_type = st.selectbox(
        "View",
        list(INDICATOR_UNITS.keys())
    )

#Stats bar chart (vertical)
try:
    r = requests.get(
        "http://web-api:4000/housing/social-indicator-stats",
        params = {"social_indicator_type": indicator_type, "year": selected_year}
    )

    if r.status_code == 200 and r.json():
        unit = INDICATOR_UNITS.get(indicator_type, "value")
        df_rank = pd.DataFrame(r.json())[["country_name", "value"]]
        df_rank["value"] = pd.to_numeric(df_rank["value"], errors = "coerce")
        df_rank = df_rank.dropna().sort_values("value", ascending = False).reset_index(drop = True)
        df_rank.columns = ["Country", f"Value ({unit})"]

        x_label = "% Change from 2015 Baseline" if indicator_type == "House Price Index" else "% of Population Impacted"
        color_scale = "ylorrd" if indicator_type == "House Price Index" else "RdYlGn_r"
        range_color = [-50, 150] if indicator_type == "House Price Index" else None

        fig = px.bar(
            df_rank,
            y = f"Value ({unit})",
            x = "Country",
            orientation = 'v',
            color = f"Value ({unit})",
            color_continuous_scale = color_scale,
            range_color = range_color,
            title = f"{indicator_type} by Country ({selected_year})",
            labels = {f"Value ({unit})": x_label}
        )

        fig.update_layout(
            yaxis = dict(),
            xaxis = dict(tickangle = 45, dtick = 1, tickfont = dict(size = 14)),
            bargap = .2,
            height = 600,
            coloraxis_showscale = False,
            showlegend = False
        )

        st.plotly_chart(fig, use_container_width = True)

    else:
        st.info("No data for this year.")


except Exception as e:
    st.error(f"Error loading rankings: {e}")

