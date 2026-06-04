import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Available listings')

# # You can access the session state to make a more customized/personalized app experience
# # get a list of all countries
# listings = requests.get('http://web-api:4000/housing/listing').json()

# for listing in listings:
#     with st.container(border=True):
#         col1, col2 = st.columns([3, 1])

#         with col1:
#             st.subheader(listing['title'])
#             st.write(f"📍 {listing['city_name']}, {listing['country_id']}")
#             st.write(f"🏠 {listing['property_type']}")

#         with col2:
#             st.metric(label="Price", value=f"€{listing['price']:,}")
#             if st.button("View Details", key=f"listing_{listing['listing_id']}"):
#                 st.session_state['listing_id'] = listing['listing_id']
#                 st.switch_page('pages/listing_details.py')

#     st.write("")
