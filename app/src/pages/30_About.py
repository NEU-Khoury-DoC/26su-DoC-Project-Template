import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    Understanding who influences EU policy, and how much they spend doing it, is really hard to figure out. Lobbying data is technically available to the public, but it's scattered, confusing, and pretty inaccessible for most people. We are building a web application to address the lack of lobbying transparency by letting users search any policy area and immediately see which organizations are lobbying on it, how much money they are spending, where they’re from, and what industry they represent.
    
    To make the analysis more meaningful, we're combining lobbying data from LobbyFacts.eu with World Bank API data including GDP, population, and government transparency scores, to add economic and political context to the lobbying patterns we're uncovering.
   
    Our app is designed for three types of users: investigative journalists following the money, political science researchers looking for patterns, and everyday citizens who just want to understand who is shaping the policies that affect them.
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
