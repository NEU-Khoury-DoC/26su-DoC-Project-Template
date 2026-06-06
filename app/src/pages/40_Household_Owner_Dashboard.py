import logging

logger = logging.getLogger(__name__)

from modules.zeus_api import get_electricity_forecast
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

st.subheader("30-Day Electricity Price Forecast")

COUNTRY_OPTIONS = {
    "Austria": "AT", "Belgium": "BE", "Bulgaria": "BG",
    "Croatia": "HR", "Czech Republic": "CZ", "Spain": "ES",
    "France": "FR", "Germany": "DE", "Hungary": "HU",
    "Latvia": "LV", "Netherlands": "NL", "Poland": "PL",
    "Portugal": "PT", "Romania": "RO", "Slovakia": "SK"
}

selected_country_name = st.selectbox(
    "Select a country:",
    options=list(COUNTRY_OPTIONS.keys()),
    index=list(COUNTRY_OPTIONS.keys()).index("Germany")
)

selected_country_code = COUNTRY_OPTIONS[selected_country_name]

try:
    data = get_electricity_forecast(selected_country_code)

    forecast_df = pd.DataFrame(data["forecast"])
    forecast_df["date"] = pd.to_datetime(forecast_df["date"])

    forecast_chart = px.scatter(
        forecast_df,
        x="date",
        y="predicted_price_eur_mwh",
        title=f"30-Day Electricity Price Forecast — {selected_country_name}",
        labels={
            "date": "Date",
            "predicted_price_eur_mwh": "Predicted Price (EUR/MWh)"
        },
    )
    forecast_chart.update_traces(
        marker=dict(size=9),
        hovertemplate="<b>%{x|%B %d, %Y}</b><br>Price: €%{y:.2f}/MWh<extra></extra>"
    )
    forecast_chart.update_layout(
        height=420,
        xaxis_title="Date",
        yaxis_title="Predicted Price (EUR/MWh)",
        hovermode="closest"
    )
    st.plotly_chart(forecast_chart, use_container_width=True)

except Exception as e:
    st.warning("Could not connect to the backend. Showing placeholder data.")

    forecast_dates = pd.date_range(
        start=pd.Timestamp.today().normalize(),
        periods=30,
        freq="D",
    )
    base_price = 0.28
    forecast_df = pd.DataFrame({
        "Date": forecast_dates,
        "Predicted Price (€/kWh)": [
            round(base_price * (1 + 0.032 * i / 29) + 0.01 * ((i % 7) - 3) / 100, 4)
            for i in range(30)
        ],
    })
    forecast_chart = px.scatter(
        forecast_df,
        x="Date",
        y="Predicted Price (€/kWh)",
        title="ML Predicted Household Energy Price (Placeholder)",
        labels={"Date": "Time", "Predicted Price (€/kWh)": "Price (€/kWh)"},
    )
    forecast_chart.update_traces(marker=dict(size=9))
    forecast_chart.update_layout(height=420)
    st.plotly_chart(forecast_chart, use_container_width=True)
