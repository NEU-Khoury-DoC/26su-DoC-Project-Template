import logging
logger = logging.getLogger(__name__)

import hashlib

import numpy as np
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Electricity Price Forecast")
st.write("#### 30-day model forecast")
st.caption("Placeholder forecast — illustrative values until the model is wired in.")

# The forecast model currently only covers Germany, so there is no selector.
selected_country = "Germany"

st.divider()

# Deterministic placeholder forecast: stable per country, but distinct.
seed = int(hashlib.md5(selected_country.encode()).hexdigest(), 16) % (2 ** 32)
rng = np.random.default_rng(seed)
base = 80 + seed % 60                     # starting price ~80-140 €/MWh
walk = rng.normal(0, 3, 30).cumsum()      # day-to-day drift
trend = np.linspace(0, rng.uniform(-20, 20), 30)
prices = np.clip(base + trend + walk, 0, None).round(1)

days = pd.date_range(pd.Timestamp.today().normalize(), periods=30)
forecast = pd.DataFrame({"Forecast price (€/MWh)": prices}, index=days)

# Headline numbers
c1, c2, c3 = st.columns(3)
c1.metric("Current", f"€{prices[0]:.0f}/MWh")
c2.metric("In 30 days", f"€{prices[-1]:.0f}/MWh", f"{prices[-1] - prices[0]:+.0f}")
c3.metric("Forecast range", f"€{prices.min():.0f}–{prices.max():.0f}/MWh")

st.write(f"### {selected_country} — next 30 days")
st.line_chart(forecast)

st.divider()

# Cross-page navigation
nav_left, nav_right = st.columns(2)
with nav_left:
    if st.button("← Back to Country Snapshot", use_container_width=True):
        st.switch_page('pages/Country_Snapshot.py')
with nav_right:
    if st.button("Gas Storage Risk →", type='primary', use_container_width=True):
        st.switch_page('pages/Gas_Storage_Risk.py')
