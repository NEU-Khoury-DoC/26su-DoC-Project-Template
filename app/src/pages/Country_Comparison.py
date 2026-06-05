import logging
logger = logging.getLogger(__name__)

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from modules.nav import SideBarLinks
from modules.zeus_api import compare_storage_risk

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Country Comparison")
st.write("#### Which countries should you worry about this winter?")

try:
    payload = compare_storage_risk()
except requests.exceptions.HTTPError as exc:
    st.error(f"Could not load risk comparison from the API: {exc}")
    st.info("Ensure the API and database are running, then seed data with `docker compose exec api python scripts/seed_gas_storage.py`.")
    st.stop()
except requests.exceptions.RequestException as exc:
    st.error(f"Could not reach the API: {exc}")
    st.stop()

latest = pd.DataFrame(payload["countries"])
latest["Country"] = latest["country_name"]
latest["Verdict"] = latest["verdict"]

at_risk_df = latest[latest["Verdict"] == "At risk"].sort_values(
    "risk_prob", ascending=False)
n_risk = len(at_risk_df)
n_total = len(latest)

if n_risk == 0:
    st.success(
        f"✅ **No countries flagged** — the model predicts all {n_total} "
        f"covered countries keep gas storage above 30% this winter."
    )
else:
    riskiest = at_risk_df.iloc[0]
    st.error(
        f"⚠️ **{n_risk} / {n_total} countries flagged**:  the model predicts "
        f"{', '.join(at_risk_df['Country'])} could see gas storage fall below "
        f"30% this winter. Highest risk: {riskiest['Country']} "
        f"({riskiest['risk_prob']:.0%})."
    )

st.caption(
    "Based on each country's most recent pre-winter storage conditions, "
    "using the same model as the Gas Storage Risk page."
)

st.divider()

st.write("### All countries, ranked by risk")

default_country = st.session_state.get("journalist_country", "Poland")
all_countries = sorted(latest["Country"])
defaults = [c for c in [default_country, "Germany", "France"] if c in all_countries]
selected_countries = st.multiselect(
    "Filter countries",
    all_countries,
    default=list(dict.fromkeys(defaults)),
)

shown = latest if not selected_countries else (
    latest[latest["Country"].isin(selected_countries)])
shown = shown.sort_values("risk_prob", ascending=True)

fig = px.bar(
    shown, x="risk_prob", y="Country", orientation="h", color="Verdict",
    color_discrete_map={"At risk": "red", "Not at risk": "steelblue"},
    labels={"risk_prob": "Chance of storage falling below 30%"},
)
fig.update_xaxes(tickformat=".0%", range=[0, 1])
fig.add_vline(x=0.5, line_dash="dash", line_color="gray")
fig.update_layout(height=max(300, 35 * len(shown)), showlegend=False)

st.plotly_chart(fig, use_container_width=True)
st.caption(
    "Longer bar = higher chance of a stressed winter and Red countries cross the line "
    "the 50% line and are flagged as at-risk"
)

with st.expander("View the data behind the rankings"):
    table = (shown.sort_values("risk_prob", ascending=False)
             [["Country", "winter", "risk_prob", "storage_at_start",
               "storage_trend_30d", "storage_volatility"]]
             .rename(columns={
                 "winter": "Winter",
                 "risk_prob": "Risk probability",
                 "storage_at_start": "Storage entering winter (%)",
                 "storage_trend_30d": "Change over final month (points)",
                 "storage_volatility": "Volatility (past 90 days)",
             })
             .set_index("Country")
             .round(2))
    st.dataframe(table, use_container_width=True)
    st.caption(
        "These three columns are the model's only inputs. Countries are "
        "shown for their most recent complete winter in the database."
    )

st.divider()

nav_left, nav_right = st.columns(2)
with nav_left:
    if st.button("← Back to Country Snapshot", use_container_width=True):
        st.switch_page('pages/Country_Snapshot.py')
with nav_right:
    if st.button("Gas Storage Risk →", type='primary', use_container_width=True):
        st.switch_page('pages/Gas_Storage_Risk.py')
