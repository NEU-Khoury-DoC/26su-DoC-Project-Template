import logging
logger = logging.getLogger(__name__)

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from modules.nav import SideBarLinks
from modules.zeus_api import get_storage_winters, post_storage_risk

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Gas Storage Risk")
st.write("#### Will storage fall below 30% this winter?")
st.caption(
    "Logistic regression trained on GIE AGSI storage data, winters 2015–2024. "
    "Adjust the inputs to explore what-if scenarios."
)

COUNTRIES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Czech Republic",
    "Denmark", "France", "Germany", "Hungary", "Italy",
    "Latvia", "Netherlands", "Poland", "Portugal", "Romania",
    "Slovakia", "Spain",
]

NAME_TO_CODE = {
    "Austria": "AT", "Belgium": "BE", "Bulgaria": "BG", "Croatia": "HR",
    "Czech Republic": "CZ", "Denmark": "DK", "France": "FR", "Germany": "DE",
    "Hungary": "HU", "Italy": "IT", "Latvia": "LV", "Netherlands": "NL",
    "Poland": "PL", "Portugal": "PT", "Romania": "RO", "Slovakia": "SK",
    "Spain": "ES",
}

RISK_THRESHOLD = 30  # %

default_country = st.session_state.get("journalist_country", "Poland")
selected_country = st.selectbox(
    "Country",
    COUNTRIES,
    index=COUNTRIES.index(default_country) if default_country in COUNTRIES else 0,
)
st.session_state["journalist_country"] = selected_country

code = NAME_TO_CODE[selected_country]

try:
    country_winters = get_storage_winters(code)
except requests.exceptions.RequestException as exc:
    st.error(f"Could not load winter data from the API: {exc}")
    st.info(
        "Ensure the API and database are running, then seed data with "
        "`docker compose exec api python scripts/seed_gas_storage.py`."
    )
    st.stop()

if not country_winters:
    st.warning("No winter records in the database for this country.")
    st.stop()

latest = max(country_winters, key=lambda row: row["winter"])

st.divider()

st.write("#### Model inputs")
st.caption(
    "Defaults show the country's most recent winter. Drag to explore different scenarios."
)

c1, c2, c3 = st.columns(3)

storage_at_start = c1.slider(
    "Storage level entering winter (%)", 0.0, 100.0,
    value=float(latest["storage_at_start"]),
    help="Average % full during October, just before winter begins Nov 1.",
)

storage_trend_30d = c2.slider(
    "Change in storage over October (points)", -30.0, 30.0,
    value=float(latest["storage_trend_30d"]),
    help="How much the storage level rose or fell during the 30 days before "
         "winter. +10 means it climbed from e.g. 80% to 90% full (still filling); "
         "negative means it was already draining.",
)

storage_volatility = c3.slider(
    "Storage volatility (past 90 days)", 0.0, 30.0,
    value=float(latest["storage_volatility"]),
    help="How much the storage level bounced around in the 90 days before winter "
         "(standard deviation). Higher = more erratic filling/draining.",
)

if storage_trend_30d >= 0:
    c2.caption(f"Filling: +{storage_trend_30d:.1f} points in the final month")
else:
    c2.caption(f"Draining: {storage_trend_30d:.1f} points in the final month")

try:
    risk_result = post_storage_risk(
        storage_at_start=storage_at_start,
        storage_trend_30d=storage_trend_30d,
        storage_volatility=storage_volatility,
    )
except requests.exceptions.RequestException as exc:
    st.error(f"Risk prediction failed: {exc}")
    st.stop()

at_risk = bool(risk_result["at_risk"])
risk_prob = float(risk_result["risk_prob"])

if at_risk:
    st.error(
        f"⚠️ **At risk** — the model predicts {selected_country}'s gas storage "
        f"would fall below {RISK_THRESHOLD}% this winter."
    )
else:
    st.success(
        f"✅ **Not at risk** — the model predicts {selected_country}'s gas storage "
        f"would stay above {RISK_THRESHOLD}% this winter."
    )

st.metric("Risk probability", f"{risk_prob:.0%}")

st.divider()

st.write("#### A full tank doesn't mean a safe winter")

try:
    all_winters = get_storage_winters()
except requests.exceptions.RequestException as exc:
    st.error(f"Could not load winter history: {exc}")
    st.stop()

plot_df = pd.DataFrame(all_winters)
plot_df["outcome"] = plot_df["storage_stress"].map({0: "No stress", 1: "Stress"})

fig = px.scatter(
    plot_df, x="storage_at_start", y="min_winter_full", color="outcome",
    color_discrete_map={"No stress": "steelblue", "Stress": "red"},
    hover_data=["country", "winter"],
    labels={"storage_at_start": "Storage % at start of winter",
            "min_winter_full": "Minimum storage % during winter"},
)
fig.add_hline(y=30, line_dash="dash", line_color="red",
              annotation_text="30% stress threshold")

mask = plot_df["country"] == code
fig.add_scatter(
    x=plot_df[mask]["storage_at_start"],
    y=plot_df[mask]["min_winter_full"],
    mode="markers",
    marker=dict(size=14, symbol="circle-open", color="black"),
    name=selected_country,
)

scenario_color = "red" if at_risk else "green"
fig.add_vline(
    x=storage_at_start,
    line_dash="dot",
    line_width=2,
    line_color=scenario_color,
    annotation_text=f"Your scenario — {risk_prob:.0%} risk",
    annotation_position="top",
    annotation_font_color=scenario_color,
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

nav_left, nav_right = st.columns(2)
with nav_left:
    if st.button("← Back to Country Snapshot", use_container_width=True):
        st.switch_page('pages/Country_Snapshot.py')
with nav_right:
    if st.button("Price Forecast →", type='primary', use_container_width=True):
        st.switch_page('pages/Price_Forecast.py')

st.divider()
st.write("#### Why we Chose 30%? ")
st.write(
    "We chose 30% as our stress threshold because it is both relevant "
    "and physically meaningful. After the 2022 gas crisis, the EU set a 90% "
    "storage mandate by November 1, and since then many EU policy analysts "
    "have treated roughly 28–30% as the level to start worrying about. There "
    "is also a physical reason to this because as storage empties, gas pressure drops, which "
    "slows the rate at which gas can be withdrawn is not being able to keep up with demand."
)
