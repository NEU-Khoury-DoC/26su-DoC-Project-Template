import logging
logger = logging.getLogger(__name__)

import hashlib

import altair as alt
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Country Comparison")
st.write("#### Compare energy indicators side by side")
st.caption("Placeholder data — indicators map to Eurostat / Ember / AGSI once wired in.")

COUNTRIES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus",
    "Czech Republic", "Denmark", "Estonia", "Finland", "France",
    "Germany", "Greece", "Hungary", "Ireland", "Italy",
    "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
    "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
    "Spain", "Sweden",
]

# Indicator -> (min, max) used only to generate stable placeholder values.
INDICATORS = {
    "Electricity Price (€/MWh)": (60, 160),
    "Gas Storage (%)": (0, 100),
    "Renewables Share (%)": (10, 90),
    "Import Dependence (%)": (10, 95),
}


def placeholder_value(country, indicator):
    """Deterministic placeholder so each country shows a stable, distinct value."""
    low, high = INDICATORS[indicator]
    digest = hashlib.md5(f"{country}-{indicator}".encode()).hexdigest()
    return low + int(digest, 16) % (high - low + 1)


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

# Bar chart for the chosen indicator
st.write(f"### {indicator}")
chart_df = pd.DataFrame(
    {
        "Country": selected_countries,
        "Value": [placeholder_value(c, indicator) for c in selected_countries],
    }
)
comparison_chart = (
    alt.Chart(chart_df)
    .mark_bar()
    .encode(
        x=alt.X("Country:N", sort=None, title=None),
        # Lock the value axis to start at 0 so it never shows negative numbers.
        y=alt.Y("Value:Q", scale=alt.Scale(domainMin=0), title=indicator),
        color=alt.Color("Country:N", legend=None),
    )
)
st.altair_chart(comparison_chart, use_container_width=True)

st.divider()

# Full side-by-side table across all indicators
st.write("### All indicators")
table = pd.DataFrame(
    {c: [placeholder_value(c, ind) for ind in INDICATORS] for c in selected_countries},
    index=list(INDICATORS.keys()),
)
st.dataframe(table, use_container_width=True)

st.divider()

# Cross-page navigation
nav_left, nav_right = st.columns(2)
with nav_left:
    if st.button("← Back to Country Snapshot", use_container_width=True):
        st.switch_page('pages/Country_Snapshot.py')
with nav_right:
    if st.button("View Historical Trends →", type='primary', use_container_width=True):
        st.switch_page('pages/Historical_Trends.py')
