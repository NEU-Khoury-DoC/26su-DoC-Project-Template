import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks()

st.title("Energy Trader Dashboard")
st.write("Welcome. This is your default landing page after logging in.")

st.divider()

st.subheader("Market at a glance")
st.caption("Placeholder data · will connect to live market prices and positions")

price_col, change_col, vol_col = st.columns(3)

price_col.metric(
    "Spot Price",
    "€84.20/MWh",
    help="Current day-ahead spot price.",
)
change_col.metric(
    "24h Change",
    "-2.1%",
    "vs. yesterday",
    delta_color="inverse",
    help="Change in spot price over the last 24 hours.",
)
vol_col.metric(
    "Traded Volume",
    "1.4 GWh",
    help="Volume traded across your tracked markets today.",
)
