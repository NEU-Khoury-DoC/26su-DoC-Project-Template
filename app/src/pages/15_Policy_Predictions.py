import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Policy: Crop Price Predictions")
st.write('Use the controls below to select a crop and region, then press Predict.')

st.write('## Predict crop price')

crop = st.selectbox('Crop', ['Wheat', 'Maize', 'Rice', 'Soybean', 'Cotton'])
region = st.selectbox('Country / Region', ['Belgium', 'United States', 'India', 'Nigeria', 'Brazil'])

if st.button('Predict'):
	st.info(f'Prediction placeholder — crop: {crop}, region: {region} (model not connected)')
