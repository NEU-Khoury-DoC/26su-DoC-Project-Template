import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Policy Maker, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('View Crop Map',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/12_Policy_Map.py')

if st.button('View Compare Farms',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/13_Policy_Compare.py')

if st.button('View Report Maker',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/14_Policy_Report.py')

if st.button('View Crop Price Predictions',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/15_Policy_Predictions.py')

if st.button('View Discussion Board',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/17_Policy_Blog.py')
