import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome government agency worker, {st.session_state['name']}.")
st.write('### What would you like to do today?')

if st.button('View Funding',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/11_view_funding.py')

if st.button('View Funding Drafts',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/13_funding_drafts.py')

if st.button('View Risk Heatmap',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/12_risk_heatmap.py')

if st.button('View Housing Deprivation Predictor',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/14_government_pred.py')