import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"WIP FOR POLICY ANALYSIS")
st.write('Quick analysis tools for policy makers — basic exploration and indicators.')

st.write('## Policymaker Analysis (draft)')

region = st.selectbox('Region', ['North Valley', 'East Farms', 'South Plains', 'River District', 'West Hills'])
indicator = st.selectbox('Indicator', ['Yield', 'Soil Quality', 'Water Stress', 'Market Price'])

if st.button('Run Analysis'):
	st.info(f'Running quick analysis for {region} — indicator: {indicator}. (Results are placeholders)')
	st.metric(label='Indicator value', value='N/A')
