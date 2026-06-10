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

st.title("Explore Trends")
st.write("Visualise crop observations filtered by season, crop, or water source.")

CROPS = ['vegetables', 'bulbvegetables', 'colecrops', 'Root&tuber',
         'fibre crop', 'oil seeds', 'pulses', 'millets', 'cereals', 'sugar crops']
SEASONS = ['kharif', 'rabi', 'Zaid']
WATER = ['rainfed', 'irrigated']

# fetch all data once
try:
    response = requests.get(f"{API_BASE}/user_growing/", timeout=5)
    df = pd.DataFrame(response.json())
except:
    st.error("Could not load data")
    st.stop()

col1, col2, col3 = st.columns(3)
with col1:
    crop_filter = st.selectbox("Crop", ["All"] + CROPS)
with col2:
    season_filter = st.selectbox("Season", ["All"] + SEASONS)
with col3:
    water_filter = st.selectbox("Water source", ["All"] + WATER)

st.divider()

# apply filters
filtered = df.copy()
if crop_filter != "All":
    filtered = filtered[filtered['type_of_crop'] == crop_filter]
if season_filter != "All":
    filtered = filtered[filtered['season'] == season_filter]
if water_filter != "All":
    filtered = filtered[filtered['water_source'] == water_filter]
    

st.write(f"**{len(filtered)} observations** match your filters")

if filtered.empty:
	st.info("No data matches your filters.")
else:
	chart1, chart2 = st.columns(2)

	with chart1:
		fig = px.box(filtered, x='type_of_crop', y='temp',
			color='water_source',
			title='Temperature by crop',
			labels={'type_of_crop': 'Crop', 'temp': '°C', 'water_source': 'Water source'})
		fig.update_layout(xaxis_tickangle=45)
		st.plotly_chart(fig, use_container_width=True)

	with chart2:
		fig2 = px.box(filtered, x='type_of_crop', y='relative_humidity',
			color='water_source',
			title='Humidity by crop',
			labels={'type_of_crop': 'Crop', 'relative_humidity': '%', 'water_source': 'Water source'})
		fig2.update_layout(xaxis_tickangle=45)
		st.plotly_chart(fig2, use_container_width=True)

	st.divider()

	crop_counts = filtered['type_of_crop'].value_counts().reset_index()
	crop_counts.columns = ['Crop', 'Count']
	fig3 = px.bar(crop_counts, x='Crop', y='Count',
		title='Crop distribution',
		color='Crop')
	fig3.update_layout(xaxis_tickangle=45, showlegend=False)
	st.plotly_chart(fig3, use_container_width=True)

	st.divider()

	st.subheader("Raw data")
	st.dataframe(filtered[['farm_id', 'type_of_crop', 'season', 'sown',
							'harvested', 'water_source', 'temp', 'relative_humidity']],
					use_container_width=True)