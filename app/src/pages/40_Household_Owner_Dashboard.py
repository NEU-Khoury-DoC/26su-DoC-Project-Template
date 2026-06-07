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

# Fetch forecast data to use in metrics and chart
try:
    data = get_electricity_forecast(selected_country_code)
    forecast_df = pd.DataFrame(data["forecast"])
    forecast_df["date"] = pd.to_datetime(forecast_df["date"])
    forecast_available = True
except Exception as e:
    forecast_available = False

# Compute metrics from forecast
if forecast_available:
    current_price = forecast_df["predicted_price_eur_mwh"].iloc[0]
    price_in_30d  = forecast_df["predicted_price_eur_mwh"].iloc[-1]
    pct_change    = ((price_in_30d - current_price) / current_price) * 100
    price_display = f"€{current_price:.2f}/MWh"
    change_display = f"{pct_change:+.1f}%"
    change_delta   = "next 30 days"
else:
    price_display  = "€0.28/kWh"
    change_display = "+3.2%"
    change_delta   = "next month"

price_col, change_col, bill_col = st.columns(3)

price_col.metric(
    "Current Energy Price",
    price_display,
    help="Forecasted day-ahead electricity price for tomorrow in EUR/MWh.",
)
change_col.metric(
    "Predicted Price Change",
    change_display,
    change_delta,
    delta_color="inverse",
    help="Forecasted price change over the next 30 days.",
)
bill_col.metric(
    "Time Until Next Bill",
    "12 days",
    help="Days remaining until your next energy bill is due.",
)

st.divider()

st.subheader("30-Day Electricity Price Forecast")

if forecast_available:
    forecast_chart = px.line(
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
        mode="lines+markers",
        marker=dict(size=6),
        line=dict(color="steelblue", width=2),
        hovertemplate="<b>%{x|%B %d, %Y}</b><br>Price: €%{y:.2f}/MWh<extra></extra>"
    )
    forecast_chart.update_layout(
        height=420,
        xaxis_title="Date",
        yaxis_title="Predicted Price (EUR/MWh)",
        hovermode="closest"
    )
    st.plotly_chart(forecast_chart, use_container_width=True)

else:
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
