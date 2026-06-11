import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Compare Crops")
st.write("Compare crop growing conditions across seasons, crop types, water sources, or countries.")

CROPS = ['vegetables', 'bulbvegetables', 'colecrops', 'Root&tuber',
         'fibre crop', 'oil seeds', 'pulses', 'millets', 'cereals', 'sugar crops']
SEASONS = ['kharif', 'rabi', 'Zaid']
WATER = ['rainfed', 'irrigated']
COUNTRIES = ['France', 'Romania', 'Portugal', 'Italy', 'Switzerland',
             'Spain', 'Czech Republic', 'Netherlands', 'Germany', 'Belgium',
             'Denmark', 'Austria']

OPTIONS_MAP = {
    'Season': SEASONS,
    'Crop': CROPS,
    'Water source': WATER,
    'Country': COUNTRIES
}

# fetch all data + map data once
try:
    response = requests.get(f"{API_BASE}/user_growing/", timeout=5)
    df = pd.DataFrame(response.json())
except:
    st.error("Could not load data")
    st.stop()

try:
    map_response = requests.get(f"{API_BASE}/user_growing/map-data", timeout=5)
    map_df = pd.DataFrame(map_response.json())
except:
    map_df = pd.DataFrame()

# compare controls
st.subheader("Compare settings")
col_a, col_b, col_c = st.columns(3)

with col_a:
    compare_by = st.selectbox("Compare by", list(OPTIONS_MAP.keys()))

options = OPTIONS_MAP[compare_by]

with col_b:
    option_a = st.selectbox(f"Option A", options, key="opt_a")

with col_c:
    option_b = st.selectbox(f"Option B", [o for o in options if o != option_a], key="opt_b")

# filter data for each option
def filter_df(df, compare_by, value, map_df):
    if compare_by == 'Season':
        return df[df['season'] == value], map_df
    elif compare_by == 'Crop':
        return df[df['type_of_crop'] == value], map_df
    elif compare_by == 'Water source':
        return df[df['water_source'] == value], map_df
    elif compare_by == 'Country':
        if not map_df.empty:
            farm_ids = map_df[map_df['country'] == value]['farm_id'].tolist()
            return df[df['farm_id'].isin(farm_ids)], map_df[map_df['country'] == value]
    return df, map_df

df_a, map_a = filter_df(df, compare_by, option_a, map_df)
df_b, map_b = filter_df(df, compare_by, option_b, map_df)

st.divider()

# side by side charts
left, right = st.columns(2)

def render_charts(col, data, label):
    with col:
        st.subheader(f"{label} ({len(data)} records)")

        if data.empty:
            st.info("No data available.")
            return

        # temp box plot
        fig = px.box(data, x='type_of_crop', y='temp',
            title=f'Temperature by crop — {label}',
            labels={'type_of_crop': 'Crop', 'temp': '°C'})
        fig.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

        # humidity box plot
        fig2 = px.box(data, x='type_of_crop', y='relative_humidity',
            title=f'Humidity by crop — {label}',
            labels={'type_of_crop': 'Crop', 'relative_humidity': '%'})
        fig2.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig2, use_container_width=True)

        # crop distribution
        crop_counts = data['type_of_crop'].value_counts().reset_index()
        crop_counts.columns = ['Crop', 'Count']
        fig3 = px.bar(crop_counts, x='Crop', y='Count',
            title=f'Crop distribution — {label}',
            color='Crop')
        fig3.update_layout(xaxis_tickangle=45, showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

        # avg stats
        st.metric("Avg temperature", f"{data['temp'].mean():.1f}°C")
        st.metric("Avg humidity", f"{data['relative_humidity'].mean():.1f}%")

render_charts(left, df_a, option_a)
render_charts(right, df_b, option_b)