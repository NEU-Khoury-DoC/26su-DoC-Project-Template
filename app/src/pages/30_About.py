import streamlit as st
from modules.nav import SideBarLinks
from pathlib import Path
from PIL import Image



st.set_page_config(layout='wide')

SideBarLinks()

st.write("# About EuroHome")

st.markdown(
    """
    EuroHome is a data platform helping students, real estate agents, 
    and government agencies navigate EU housing markets. Students can 
    research listings and plan their budget, real estate agents can find 
    properties and post listings, and government agencies/project managers
    can explore funding projects with Eurostat data on indicators 
    (crime, pollution, poverty, etc.) to help propose funding plan drafts. 
    """
)

st.write("# About the team")
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True, height = 850):
        img_path = Path(__file__).parent.parent / "assets" / "geo-headshot.JPG"
        st.image(str(img_path))
        st.write("##### Geo Thatch")

        st.write('Geo is an incoming sophomore at Northeastern University studying ' \
        'computer science and math. Currently taking CS 3200 and CS 4973.')
    
    with st.container(border=True, height = 850):
        img_path = Path(__file__).parent.parent / "assets" / "isabel-headshot.jpeg"
        st.image(str(img_path))
        st.write("##### Isabel Larenas")
        st.write('Isabel is an incoming junior at Northeastern University majoring in ' \
        'computer science with a minor in spanish. Currently taking DS 3000 and CS 4973.')

with col2:
    with st.container(border=True, height = 850):
        img_path = Path(__file__).parent.parent / "assets" / "maira-headshot.png"
        st.image(str(img_path))
        st.write("##### Maira Padani")
        st.write('Maira is an incoming senior at Northeastern University majoring in ' \
        'business administration with a minor in data science. Currently taking CS 3200 and CS 4973.')

    with st.container(border=True, height = 850):
        img_path = Path(__file__).parent.parent / "assets" / "laasya-headshot.jpeg"
        st.image(str(img_path))
        st.write("##### Laasya Gattu")
        st.write('Laasya is an incoming sophomore at Northeastern University majoring in ' \
        'data science and business administration with a minor in public health. Currently taking DS 3000 and CS 4973.')


# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
