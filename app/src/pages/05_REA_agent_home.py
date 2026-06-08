import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Real Estate Agent, {st.session_state['name']}.")
st.write('### What would you like to do today?')

if st.button('View market dashboard',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/06_market_dashboard.py')

if st.button('View listings',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/07_view_listings_rea.py')

if st.button('Create listing',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/08_add_listing.py')
