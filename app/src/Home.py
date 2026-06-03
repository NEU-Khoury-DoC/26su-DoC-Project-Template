##################################################
# Main entry-point for the Zeus Streamlit app
##################################################

import logging

logging.basicConfig(
    format="%(filename)s:%(lineno)s:%(levelname)s -- %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

# User is on the login page — not authenticated yet
st.session_state["authenticated"] = False

SideBarLinks(show_home=True)

logger.info("Loading the Home page of the app")

st.title("Zeus Energy Security Index")
st.write("Choose a persona, then log in.")

col_household, col_journalist, col_analyst, col_login = st.columns([2, 2, 2, 1])

with col_household:
    st.markdown("**Household Owner**")
    st.selectbox(
        "Household Owner options",
        options=["Select an option", "Option 1", "Option 2"],
        key="household_owner_dropdown",
        label_visibility="collapsed",
    )

with col_journalist:
    st.markdown("**Journalist**")
    st.selectbox(
        "Journalist options",
        options=["Select an option", "Option 1", "Option 2"],
        key="journalist_dropdown",
        label_visibility="collapsed",
    )

with col_analyst:
    st.markdown("**Analyst**")
    st.selectbox(
        "Analyst options",
        options=["Select an option", "Option 1", "Option 2"],
        key="analyst_dropdown",
        label_visibility="collapsed",
    )

with col_login:
    st.markdown("&nbsp;", unsafe_allow_html=True)
    st.button("Log in", type="primary", use_container_width=True)
