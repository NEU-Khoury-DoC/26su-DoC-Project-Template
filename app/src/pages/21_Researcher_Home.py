import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Researcher, {st.session_state['first_name']}.")
st.write('### What would you like to do today?')

if st.button('View Dashboard',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/22_Researcher_Dashboard.py')

if st.button('View Map',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/23_Researcher_Map.py')

if st.button('View Explore Crop Conditions',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/24_Researcher_Conditions.py')

if st.button('View Explore Trends',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/25_Researcher_Trends.py')

if st.button('View Compare',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/31_Researcher_Compare.py')

if st.button('View Generate Reports',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/26_Researcher_Report.py')

if st.button('View Data Export',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/27_Researcher_Data_Export.py')

if st.button('View Discussion Board',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/28_Researcher_Blog.py')
