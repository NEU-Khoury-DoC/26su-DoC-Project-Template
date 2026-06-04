import streamlit as st
from PIL import Image
from pathlib import Path
from modules.nav import SideBarLinks

# Build absolute path to static/ relative to this file's location
# pages/about.py → parent = pages/ → parent = project root → static/
STATIC = Path(__file__).parent.parent / "assets"

st.set_page_config(layout='wide')

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    Understanding who influences EU policy, and how much they spend doing it, is really hard to figure out. Lobbying data is technically available to the public, but it's scattered, confusing, and pretty inaccessible for most people. We are building a web application to address the lack of lobbying transparency by letting users search any policy area and immediately see which organizations are lobbying on it, how much money they are spending, where they're from, and what industry they represent.
    
    To make the analysis more meaningful, we're combining lobbying data from LobbyFacts.eu with World Bank API data including GDP, population, and government transparency scores, to add economic and political context to the lobbying patterns we're uncovering.
   
    Our app is designed for three types of users: investigative journalists following the money, political science researchers looking for patterns, and everyday citizens who just want to understand who is shaping the policies that affect them.
    """
)

st.markdown("---")
st.write("## Authors")

col1, col2, col3, col4 = st.columns(4)

with col1:
    img = Image.open(STATIC / "Alyssa_Headshot.jpeg")
    w, h = img.size; side = min(w, h)
    img = img.crop(((w-side)//2, (h-side)//2, (w+side)//2, (h+side)//2))
    st.image(img, use_container_width=True)
    st.markdown("### Alyssa D.")
    st.caption("CS · Frontend & Data Modeling")
    st.markdown(
        """
        Responsible for the ER diagrams, wireframes, and frontend pages.
        Focused on making the app accessible and intuitive for all three user personas.
        """
    )

with col2:
    img = Image.open(STATIC / "Manav_Headshot.png")
    w, h = img.size; side = min(w, h)
    img = img.crop(((w-side)//2, (h-side)//2, (w+side)//2, (h+side)//2))
    st.image(img, use_container_width=True)
    st.markdown("### Manav")
    st.caption("CS · Backend & Database")
    st.markdown(
        """
        Built the SQL DDL, database schema, and Flask REST API routes.
        Focused on data integrity and connecting the backend to the frontend.
        """
    )

with col3:
    img = Image.open(STATIC / "Mihika_Headshot.jpeg")
    w, h = img.size; side = min(w, h)
    img = img.crop(((w-side)//2, (h-side)//2, (w+side)//2, (h+side)//2))
    st.image(img, use_container_width=True)
    st.markdown("### Mihika")
    st.caption("DS · Machine Learning")
    st.markdown(
        """
        Led the ML model development, including data cleaning, feature engineering,
        and building the lobbying influence prediction model.
        """
    )

with col4:
    img = Image.open(STATIC / "Rishi_Headshot.jpeg")
    w, h = img.size; side = min(w, h)
    img = img.crop(((w-side)//2, (h-side)//2, (w+side)//2, (h+side)//2))
    st.image(img, use_container_width=True)
    st.markdown("### Rishi")
    st.caption("DS · Data & Visualization")
    st.markdown(
        """
        Handled data sourcing from LobbyFacts and the World Bank API,
        EDA, and data visualizations used throughout the app.
        """
    )

st.markdown("---")

if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")