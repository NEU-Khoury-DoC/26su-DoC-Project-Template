import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"WIP FOR POLICY BLOG")
st.write('Place for poicy makers to see and reply to farmer concerns and complaints')