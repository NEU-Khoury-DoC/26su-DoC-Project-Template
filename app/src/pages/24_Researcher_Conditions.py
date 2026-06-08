import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"RESEARCHER CONDITIONS")
st.write('Query current field / farm conditions and filter observations.')

col1, col2 = st.columns([3,1])

with col2:
	st.subheader('Filters')
	crop = st.selectbox('Crop', ['All', 'Wheat', 'Maize', 'Rice', 'Soybean'])
	region = st.selectbox('Region', ['All', 'North Valley', 'East Farms', 'South Plains', 'River District'])
	date_range = st.date_input('Date (single or range)')
	if st.button('Apply Filters'):
		st.experimental_rerun()

with col1:
	st.subheader('Latest Observations')
	# placeholder sample data
	import pandas as pd
	df = pd.DataFrame([
		{'date':'2024-05-01','region':'North Valley','crop':'Wheat','temp':21.3,'humidity':45},
		{'date':'2024-05-02','region':'East Farms','crop':'Maize','temp':19.1,'humidity':50},
	])
	st.dataframe(df, use_container_width=True)

st.markdown('---')
st.subheader('Condition Map')
st.write('Map placeholder')