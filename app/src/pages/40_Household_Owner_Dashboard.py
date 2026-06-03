import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks()

st.title("Household Owner Dashboard")
st.write("Welcome. This is your default landing page after logging in.")
