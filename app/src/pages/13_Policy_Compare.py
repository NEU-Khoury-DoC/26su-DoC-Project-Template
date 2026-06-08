import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"POLICY COMPARE")
st.write('Select two farms or regions to compare key metrics side-by-side.')

col1, col2 = st.columns(2)
with col1:
	left_region = st.selectbox('Left: Region / Farm', ['North Valley', 'East Farms', 'South Plains', 'River District', 'West Hills'])
	left_metrics = st.multiselect('Metrics', ['Productivity', 'Soil Quality', 'Crop Price', 'Flood Risk'], default=['Productivity', 'Crop Price'], key='left_metrics')

with col2:
	right_region = st.selectbox('Right: Region / Farm', ['North Valley', 'East Farms', 'South Plains', 'River District', 'West Hills'], index=1)
	right_metrics = st.multiselect('Metrics', ['Productivity', 'Soil Quality', 'Crop Price', 'Flood Risk'], default=['Productivity', 'Crop Price'], key='right_metrics')

if st.button('Compare'):
	st.write(f'Comparing {left_region} vs {right_region}')
	# placeholder tables
	st.table({
		left_region: {'Productivity': '87%', 'Soil Quality': 82, 'Crop Price': '$6.40'},
		right_region: {'Productivity': '74%', 'Soil Quality': 70, 'Crop Price': '$4.80'}
	})