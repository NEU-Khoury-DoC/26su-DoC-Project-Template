import streamlit as st
from modules.nav import SideBarLinks
from modules.community_feed import render_feed

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Discussion Board")
render_feed()