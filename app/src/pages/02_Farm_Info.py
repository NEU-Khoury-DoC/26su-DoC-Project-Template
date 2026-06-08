import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

def handle_submission(text: str, option: str) -> dict:
    """Replace this with your actual backend logic."""
    return {"received_text": text, "received_option": option}


st.title(f"FARM INFO")
st.write('Enter or edit basic information about your farm. This is a UI draft / not wired yet.')

col1, col2 = st.columns(2)
with col1:
    farm_name = st.text_input('Farm name')
    country = st.selectbox('Country', ['Belgium', 'United States', 'India', 'Nigeria'])
    latitude = st.number_input('Latitude', format='%.6f')
    longitude = st.number_input('Longitude', format='%.6f')

with col2:
    main_crops = st.multiselect('Main crops', ['Wheat', 'Maize', 'Rice', 'Soybean', 'Cotton'])
    area = st.number_input('Area (hectares)', min_value=0.0, format='%.2f')
    irrigation = st.selectbox('Irrigation type', ['None', 'Surface', 'Sprinkler', 'Drip'])

if st.button('Save Farm Info'):
    result = handle_submission(farm_name, country)
    st.success('Farm info saved (UI placeholder).')
    st.json({
        'farm_name': farm_name,
        'country': country,
        'lat': latitude,
        'lon': longitude,
        'main_crops': main_crops,
        'area_ha': area,
        'irrigation': irrigation,
        'backend_response': result,
    })

