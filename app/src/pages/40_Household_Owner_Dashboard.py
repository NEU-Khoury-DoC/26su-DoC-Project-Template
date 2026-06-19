import logging

logger = logging.getLogger(__name__)

import pandas as pd
import plotly.express as px
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks()

st.title("Household Owner Dashboard")
st.write("Welcome. This is your default landing page after logging in.")

st.divider()

st.subheader("Your energy at a glance")
st.caption("Placeholder data · will connect to live price forecasts and billing cycle")

price_col, change_col, bill_col = st.columns(3)

price_col.metric(
    "Current Energy Price",
    "€0.28/kWh",
    help="Your household's current electricity rate.",
)
change_col.metric(
    "Predicted Price Change",
    "+3.2%",
    "next month",
    delta_color="inverse",
    help="Forecasted change in your energy price over the next billing period.",
)
bill_col.metric(
    "Time Until Next Bill",
    "12 days",
    help="Days remaining until your next energy bill is due.",
)

st.divider()

st.subheader("Predicted Energy Price Forecast")
# Placeholder daily predictions until the ML model endpoint is wired in.
forecast_dates = pd.date_range(
    start=pd.Timestamp.today().normalize(),
    periods=30,
    freq="D",
)
base_price = 0.28
forecast_df = pd.DataFrame(
    {
        "Date": forecast_dates,
        "Predicted Price (€/kWh)": [
            round(base_price * (1 + 0.032 * i / 29) + 0.01 * ((i % 7) - 3) / 100, 4)
            for i in range(30)
        ],
    }
)

forecast_chart = px.scatter(
    forecast_df,
    x="Date",
    y="Predicted Price (€/kWh)",
    title="ML Predicted Household Energy Price",
    labels={"Date": "Time", "Predicted Price (€/kWh)": "Price (€/kWh)"},
)
forecast_chart.update_traces(marker=dict(size=9))
forecast_chart.update_layout(height=420, xaxis_title="Time", yaxis_title="Price (€/kWh)")
st.plotly_chart(forecast_chart, use_container_width=True)
