import logging
logger = logging.getLogger(__name__)

import pandas as pd
import plotly.express as px
import streamlit as st
from modules.nav import SideBarLinks
from modules import entsoe_data

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Country Snapshot")
st.write("#### Ten years of gas storage, one country at a time")

# ---- Load data (cached) ----
@st.cache_data
def load_history():
    df = pd.read_csv("assets/agsi_clean.csv", parse_dates=["gasDayStart"])
    return df[["country", "gasDayStart", "full"]]

@st.cache_data
def load_winters():
    return pd.read_csv("assets/dataset.csv")

history = load_history()
winters = load_winters()

NAME_TO_CODE = {
    "Austria": "AT", "Belgium": "BE", "Bulgaria": "BG", "Croatia": "HR",
    "Czech Republic": "CZ", "Denmark": "DK", "France": "FR", "Germany": "DE",
    "Hungary": "HU", "Italy": "IT", "Latvia": "LV", "Netherlands": "NL",
    "Poland": "PL", "Portugal": "PT", "Romania": "RO", "Slovakia": "SK",
    "Spain": "ES",
}
COUNTRIES = list(NAME_TO_CODE.keys())
STRESS_THRESHOLD = 30

# Persist country selection so the other journalist pages can read it.
default_country = st.session_state.get("journalist_country", "Poland")
selected_country = st.selectbox(
    "Select Country",
    COUNTRIES,
    index=COUNTRIES.index(default_country) if default_country in COUNTRIES else 0,
)
st.session_state["journalist_country"] = selected_country

code = NAME_TO_CODE[selected_country]
country_hist = history[history["country"] == code].sort_values("gasDayStart")
country_winters = winters[winters["country"] == code]

st.divider()

# ---- Headline numbers ----
st.subheader(selected_country)

latest_row = country_hist.iloc[-1]
month_ago = country_hist[
    country_hist["gasDayStart"] <= latest_row["gasDayStart"] - pd.Timedelta(days=30)
]
delta_30d = (latest_row["full"] - month_ago.iloc[-1]["full"]) if len(month_ago) else None

stress_count = int(country_winters["storage_stress"].sum())
total_winters = len(country_winters)
worst = country_winters["min_winter_full"].min()

m1, m2, m3, m4 = st.columns(4)
m1.metric(
    "Storage level",
    f"{latest_row['full']:.0f}%",
    f"{delta_30d:+.0f} points past 30 days" if delta_30d is not None else None,
)
m2.metric("Stressed winters", f"{stress_count} of {total_winters}")
m3.metric("Lowest winter level on record", f"{worst:.0f}%")
m4.metric("Stress threshold", f"{STRESS_THRESHOLD}%")
st.caption(
    f"Latest reported value: {latest_row['gasDayStart'].date()} · "
    "GIE AGSI transparency platform"
)

st.divider()

# ---- Storage history ----
st.write(f"##### How {selected_country} fills and drains its storage")

fig = px.line(
    country_hist, x="gasDayStart", y="full",
    labels={"gasDayStart": "", "full": "Storage % full"},
)
fig.add_hline(
    y=STRESS_THRESHOLD, line_dash="dash", line_color="red",
    annotation_text="30% stress threshold",
)
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)
st.caption(
    "The pattern is the seasonal cycle: fill through summer, drain "
    "through winter. Note how close the fill gets to the red line"
)

st.divider()

# ---- Context for reporting ----
st.write("##### Context for your story")

if stress_count > 0:
    worst_winter = country_winters.loc[
        country_winters["min_winter_full"].idxmin(), "winter"
    ]
    st.write(
        f"{selected_country} has dipped below the 30% line in "
        f"{stress_count} of the last {total_winters} winters. The closest "
        f"call was the winter of {int(worst_winter)}, when storage bottomed "
        f"out at {worst:.0f}%. Worth asking national regulators what changed "
        "since."
    )

st.write(
    "Since the 2022 gas crisis, EU rules require storage to be 90% full by "
    "November 1 each year.  "
    "A country can enter winter full and still drain fast if it "
    "depends heavily on imports or has a cold snap."
)

# ---- Recommendations ----
st.write("##### Recommendations")

current_level = latest_row["full"]

if current_level < 40:
    st.warning(
        f"**Storage is running low ({current_level:.0f}%).** Angles worth "
        "pursuing now: whether the country is buying LNG on the spot market "
        "to compensate (and at what price), whether neighbors are sending gas "
        "through interconnectors, and whether officials are discussing demand "
        "reduction measures. Ask the energy ministry how they plan to hit the "
        "EU's 90% refill target by November 1, refilling from a low base is "
        "expensive, and that cost lands on consumers."
    )
elif current_level < 70:
    st.info(
        f"**Storage is mid-range ({current_level:.0f}%).** The story here is "
        "the refill race: track whether the level climbs steadily toward the "
        "EU's 90% November 1 target over the coming months. A flat or falling "
        "line in summer is unusual and worth a phone call, it can signal "
        "high prices discouraging refills or strong export demand."
    )
else:
    st.success(
        f"**Storage is comfortable ({current_level:.0f}%).** Low urgency, but "
        "two angles still work: what filling storage this full costs and who "
        "pays for it, and whether a full tank actually guarantees a safe "
        "winter, our model shows it often doesn't."
    )

if stress_count > 0:
    st.write(
        f"Because {selected_country} has a history of stressed winters "
        f"({stress_count} of {total_winters}), it's worth building a source "
        "relationship with the national TSO and storage operators before "
        "winter, not during the crisis. Past coverage of the "
        f"{int(worst_winter)} winter is your best background reading."
    )

st.write("")
left, right = st.columns(2)

with left:
    st.write("**Watch these through the season**")
    st.markdown(
        "- [GIE AGSI](https://agsi.gie.eu) — the live version of this page's "
        "data, updated daily\n"
        "- [EC gas storage policy](https://energy.ec.europa.eu/topics/energy-security/gas-storage_en) "
        "— the 90% mandate and compliance tracking\n"
        "- National TSO announcements — supply warnings appear here first"
    )

with right:
    st.write("**Background for a deeper piece**")
    st.markdown(
        "- [Eurostat import dependency](https://ec.europa.eu/eurostat/databrowser/product/page/nrg_ind_id) "
        "— who's most exposed to supply shocks\n"
        "- [Ember](https://ember-energy.org/data/) — prices and electricity "
        "mix, if the story widens beyond gas\n"
        "- [ENTSOG](https://www.entsog.eu) — how gas physically moves "
        "between countries"
    )



st.divider()

# Cross-page navigation
nav_left, nav_right = st.columns(2)
with nav_left:
    if st.button("Gas Storage Risk →", type='primary', use_container_width=True):
        st.switch_page('pages/Gas_Storage_Risk.py')
with nav_right:
    if st.button("Compare Countries →", use_container_width=True):
        st.switch_page('pages/Country_Comparison.py')