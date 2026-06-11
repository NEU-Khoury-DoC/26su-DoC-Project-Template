import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide', page_title="About FarmCast")
SideBarLinks()

st.title("About FarmCast")
st.divider()

# What is FarmCast
st.markdown("## What is FarmCast?")
st.write("""
YOUR DESCRIPTION HERE
""")

st.divider()

# Team
st.markdown("## Meet the Team")

r1, r2= st.columns(2)

with r1:
    st.image("assets/headshots/headshot.jpg", width=300)
    st.markdown("**NICOLE STEKOL**")
    st.write("Short bio or description here.")

with r2:
    st.image("assets/headshots/IMG_2392.JPG", width=200)
    st.markdown("**LAURYN GONG**")
    st.write("Hi, I’m Lauryn Gong! I’m a rising second year student at Northeastern studying computer science and business!")


r3, r4= st.columns(2)

with r3:
   # st.image("assets/team3.png", width=150)
    st.markdown("**ELISE WIZEMANN**")
    st.write("Short bio or description here.")

with r4:
 #   st.image("assets/team4.png", width=150)
    st.markdown("**MINJU SUNG**")
    st.write("Short bio or description here.")

st.divider()

# Data sources
st.markdown("## Data Sources")

ds1, ds2 = st.columns(2)

with ds1:
    st.markdown("#### 📊 Eurostat")
    st.write("YOUR EUROSTAT DESCRIPTION HERE")
    st.markdown("[eurostat.ec.europa.eu](https://ec.europa.eu/eurostat)")

with ds2:
    st.markdown("#### 🌤 Open-Meteo")
    st.write("YOUR OPEN-METEO DESCRIPTION HERE")
    st.markdown("[open-meteo.com](https://open-meteo.com)")

st.divider()
st.caption("FarmCast — Built as part of a data systems course.")

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
