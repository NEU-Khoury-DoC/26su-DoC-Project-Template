import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Student, {st.session_state['name']}.")
st.write('### What would you like to do today?')

if st.button('View listings',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_view_listings_student.py')

if st.button('View budget manager',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_budget_manager.py')
