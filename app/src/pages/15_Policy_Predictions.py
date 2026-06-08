import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Policy: Crop Price Predictions")
st.write('Use the controls below to select a crop and region, then press Predict.')

st.write('## Predict crop price')

crop = st.selectbox('Crop', ['Barley', 'Durum Wheat', 'Feed Barley', 'Rye', 'Soft Wheat'])
region = st.selectbox('Country / Region', ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Estonia', 'Finland', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden'])

#TODO ADD NEW ERROR FOR WHEN SOMETHING DOESNT EXIST IN DB (BARLEY IN AUSTRIA AS AN EXAMPLE)
# GERBER SAYS TO THROW A NEW ERROR INSTEAD OF A 404

if st.button('Predict'):
    logger.info(f'Prediction — crop: {crop}, region: {region}')
    try:
        response = requests.get(
            f'http://web-api:4000/prices_model/prediction/{crop}/{region}'
        )
        if response.status_code == 400:
            error = response.json().get('error', '')
            if 'Not enough price history' in error:
                st.warning(f"No price data available for {crop} in {region}. Try a different combination.")
            else:
                st.error(f"Could not make prediction: {error}")
        elif response.status_code == 200:
            pred = response.json()['prediction']
            st.success('Prediction complete!')
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(label='Crop', value=crop)
            with m2:
                st.metric(label='Country', value=region)
            with m3:
                st.metric(label='Predicted Price', value=f'€{pred:,.2f}')
        else:
            st.error(f"Unexpected error: {response.status_code}")
    except Exception as e:
        logger.error(f'Prediction error: {e}')
        st.error(f'Could not retrieve prediction: {e}')