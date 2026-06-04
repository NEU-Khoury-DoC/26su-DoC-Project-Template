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

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    country_filter = st.selectbox("Country", 
                                options=["All"] + [c['country_name'] for c in 
                                        requests.get('http://web-api:4000/housing/country').json()])
with col2:
    property_filter = st.selectbox("Property Type", 
                                options=
                                ["All", "House", "Apartment", "Studio Apartment", "Townhouse"])
with col3:
    price_filter = st.number_input("Max Price (€)", 
                                   min_value=0, max_value=3000, value=1500, step=100)
with col4:
    university_filter = st.selectbox("Associated University", 
                                options=["All"] + [u['university_name'] for u 
                                in requests.get('http://web-api:4000/housing/university').json()])
with col5:
    city_filter = st.selectbox("City", options=["All"] + [c['city_name'] for c
                                in requests.get('http://web-api:4000/housing/cities').json()])

# build params based on filters
params = {}
if country_filter != "All":
    params["country"] = country_filter
if property_filter != "All":
    params["property_type"] = property_filter
if price_filter < 5000:
    params["price"] = price_filter
if city_filter != "All":
    params["city_name"] = city_filter
if university_filter != "All":
    params["university"] = university_filter

# You can access the session state to make a more customized/personalized app experience
listings = requests.get('http://web-api:4000/housing/listing', params=params).json()

for listing in listings:
    listing['price'] = int(listing['price'])

    with st.container(border=True):
        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader(listing['title'])
        
        with col2:
            reviews = requests.get(
                f"http://web-api:4000/housing/reviews",
                params={"listing_id": listing['listing_id']}
            ).json()
            total = 0
            num = 0
            avg = 0
            for review in reviews:
                if review['rating'] is not None:
                    total += int(review['rating'])
                    num +=1
            if num > 0:
                avg = total/num
            avg = round(avg, 2)
            if avg > 0:
                st.subheader(f'{avg}/5.0')
            
        # with col2:
        #     st.subheader(f"${listing['price']} / month")

    if listing['university_name']:
        with st.container(border=False):
            col1, col2, col3= st.columns([3, 3, 2])

            with col1:
                st.write(f"📍 {listing['city_name']}, {listing['country_name']}")
                st.write(f"🏠 {listing['property_type']}")
                st.write(f"🏫 Associated with {listing['university_name']}")

            with col2:
                st.subheader(f"${listing['price']} / month")

            with col3:
                if st.button("View reviews", key=f"listing_{listing['listing_id']}"):
                    st.session_state['listing_id'] = listing['listing_id']
                    st.session_state['title'] = listing['title']
                    st.switch_page('pages/03_view_reviews.py')
    
    else:
        with st.container(border=False):
            col1, col2, col3 = st.columns([3, 3, 2])

            with col1:
                st.write(f"📍 {listing['city_name']}, {listing['country_name']}")
                st.write(f"🏠 {listing['property_type']}")

            with col2:
                st.subheader(f"${listing['price']} / month")
            
            with col3:
                if st.button("View reviews", key=f"listing_{listing['listing_id']}"):
                    st.session_state['listing_id'] = listing['listing_id']
                    st.session_state['title'] = listing['title']
                    st.switch_page('pages/03_view_reviews.py')


    st.write("")


