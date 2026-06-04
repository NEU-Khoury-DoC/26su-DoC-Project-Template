import logging
logger = logging.getLogger(__name__)

import altair as alt
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
from modules import entsoe_data

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Country Snapshot")
st.write("#### All indicators in one place")

COUNTRIES = entsoe_data.COUNTRIES

# Persist country selection so the other journalist pages can read it.
default_country = st.session_state.get("journalist_country", "Poland")
selected_country = st.selectbox(
    "Select Country",
    COUNTRIES,
    index=COUNTRIES.index(default_country) if default_country in COUNTRIES else 0,
)
st.session_state["journalist_country"] = selected_country

st.divider()

# Country header
st.subheader(selected_country)
st.caption("Live data · ENTSO-E Transparency Platform · latest available day")

if not entsoe_data.has_api_key():
    st.error(
        "No ENTSO-E API key configured. Set ENTSOE_API_KEY (env var, Streamlit "
        "secret, or datasets/entsoe/entsoe.env) to load live data."
    )
    st.stop()


def _fmt(value, unit, fmt="{:.1f}", suffix=""):
    """Format a metric value, falling back to N/A when missing."""
    if value is None:
        return "N/A"
    return f"{fmt.format(value)}{unit}{suffix}"


def _delta(delta, unit, fmt="{:+.1f}"):
    """Format a day-over-day delta for st.metric, or None to hide it."""
    if delta is None:
        return None
    return f"{fmt.format(delta)}{unit} DoD"


with st.spinner(f"Loading live ENTSO-E data for {selected_country}…"):
    price, price_d = entsoe_data.get_price(selected_country)
    demand, demand_d = entsoe_data.get_demand(selected_country)
    renew, renew_d = entsoe_data.get_renewables_share(selected_country)
    imports, imports_d = entsoe_data.get_import_dependence(selected_country)
    mix = entsoe_data.get_mix(selected_country)

# Headline indicators
m1, m2, m3, m4 = st.columns(4)
m1.metric("Electricity Price", _fmt(price, " €/MWh"), _delta(price_d, " €/MWh"))
m2.metric("Electricity Demand", _fmt(demand, " GWh", "{:.0f}"),
          _delta(demand_d, " GWh", "{:+.0f}"))
m3.metric("Renewables Share", _fmt(renew, "%"), _delta(renew_d, "pp"))
m4.metric("Import Dependence", _fmt(imports, "%"), _delta(imports_d, "pp"),
          delta_color="inverse")

st.divider()

# Where the country's electricity comes from
st.write("##### Where the electricity comes from")
if mix is None:
    st.info("Generation mix is not available for this country.")
else:
    mix_df = mix.reset_index()
    mix_df.columns = ["Source", "Share (%)"]
    mix_chart = (
        alt.Chart(mix_df)
        .mark_bar()
        .encode(
            # Lock the value axis to 0–100 so it never shows negative numbers.
            x=alt.X("Share (%):Q", scale=alt.Scale(domain=[0, 100])),
            y=alt.Y("Source:N", sort=entsoe_data.MIX_ORDER, title=None),
            tooltip=["Source", alt.Tooltip("Share (%):Q", format=".1f")],
        )
    )
    st.altair_chart(mix_chart, use_container_width=True)

st.divider()

# Cross-page navigation
nav_left, nav_right = st.columns(2)
with nav_left:
    if st.button("Gas Storage Risk →", type='primary', use_container_width=True):
        st.switch_page('pages/Gas_Storage_Risk.py')
with nav_right:
    if st.button("Compare Countries →", type='primary', use_container_width=True):
        st.switch_page('pages/Country_Comparison.py')
