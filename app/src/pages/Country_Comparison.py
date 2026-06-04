import logging
logger = logging.getLogger(__name__)

import altair as alt
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks
from modules import entsoe_data

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Country Comparison")
st.write("#### Compare energy indicators side by side")
st.caption("Live data · ENTSO-E Transparency Platform · latest available day")

COUNTRIES = entsoe_data.COUNTRIES
INDICATORS = entsoe_data.COMPARISON_INDICATORS

if not entsoe_data.has_api_key():
    st.error(
        "No ENTSO-E API key configured. Set ENTSOE_API_KEY (env var, Streamlit "
        "secret, or datasets/entsoe/entsoe.env) to load live data."
    )
    st.stop()

# Filters
filter_left, filter_right = st.columns([3, 2])

with filter_left:
    default_country = st.session_state.get("journalist_country", "Poland")
    defaults = [c for c in [default_country, "Germany", "France"] if c in COUNTRIES]
    selected_countries = st.multiselect(
        "Countries to compare",
        COUNTRIES,
        default=list(dict.fromkeys(defaults)),
    )

with filter_right:
    indicator = st.selectbox("Indicator", list(INDICATORS.keys()))

st.divider()

if not selected_countries:
    st.info("Select at least one country to compare.")
    st.stop()


@st.cache_data(ttl=3600, show_spinner=False)
def indicator_table(countries):
    """Wide table of every indicator for the chosen countries (rows=indicator)."""
    data = {
        c: [entsoe_data.get_indicator_value(c, label) for label in INDICATORS]
        for c in countries
    }
    return pd.DataFrame(data, index=list(INDICATORS.keys()))


with st.spinner("Loading live ENTSO-E data…"):
    table = indicator_table(tuple(selected_countries))

# Bar chart for the chosen indicator
st.write(f"### {indicator}")
chart_df = (
    table.loc[indicator]
    .rename("Value")
    .rename_axis("Country")
    .reset_index()
    .dropna(subset=["Value"])
)
missing = [c for c in selected_countries if c not in set(chart_df["Country"])]

if chart_df.empty:
    st.info("No data available for the selected countries on this indicator.")
else:
    comparison_chart = (
        alt.Chart(chart_df)
        .mark_bar()
        .encode(
            x=alt.X("Country:N", sort=None, title=None),
            # Lock the value axis to start at 0 so it never shows negative numbers.
            y=alt.Y("Value:Q", scale=alt.Scale(domainMin=0), title=indicator),
            color=alt.Color("Country:N", legend=None),
            tooltip=["Country", alt.Tooltip("Value:Q", format=".1f")],
        )
    )
    st.altair_chart(comparison_chart, use_container_width=True)

if missing:
    st.caption("No data on this indicator for: " + ", ".join(missing))

st.divider()

# Full side-by-side table across all indicators
st.write("### All indicators")
st.dataframe(table.round(1), use_container_width=True)

st.divider()

# Cross-page navigation
nav_left, nav_right = st.columns(2)
with nav_left:
    if st.button("← Back to Country Snapshot", use_container_width=True):
        st.switch_page('pages/Country_Snapshot.py')
with nav_right:
    if st.button("Gas Storage Risk →", type='primary', use_container_width=True):
        st.switch_page('pages/Gas_Storage_Risk.py')
