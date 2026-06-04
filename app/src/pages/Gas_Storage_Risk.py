import logging
logger = logging.getLogger(__name__)

import hashlib

import numpy as np
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Gas Storage Risk")
st.write("#### Will storage fall below 30%?")
st.caption("Placeholder model output — illustrative until the model is wired in.")

# Countries covered by the gas storage model.
COUNTRIES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Czech Republic",
    "Denmark", "France", "Germany", "Hungary", "Italy",
    "Latvia", "Netherlands", "Poland", "Portugal", "Romania",
    "Slovakia", "Spain",
]

RISK_THRESHOLD = 30  # %

default_country = st.session_state.get("journalist_country", "Poland")
selected_country = st.selectbox(
    "Country",
    COUNTRIES,
    index=COUNTRIES.index(default_country) if default_country in COUNTRIES else 0,
)
st.session_state["journalist_country"] = selected_country

st.divider()

# Placeholder model output: a binary at-risk classification (stable per country).
seed = int(hashlib.md5(selected_country.encode()).hexdigest(), 16) % (2 ** 32)
rng = np.random.default_rng(seed)
current = int(rng.integers(35, 96))   # current storage % (known input, shown for context)
at_risk = bool(rng.random() < 0.4)    # the model's prediction

# Verdict
if at_risk:
    st.error(
        f"⚠️ **At risk** — the model predicts {selected_country}'s gas storage "
        f"will fall below {RISK_THRESHOLD}% within 30 days."
    )
else:
    st.success(
        f"✅ **Not at risk** — the model predicts {selected_country}'s gas storage "
        f"will stay above {RISK_THRESHOLD}% over the next 30 days."
    )

st.metric("Current storage", f"{current}%")

st.divider()

# Cross-page navigation
nav_left, nav_right = st.columns(2)
with nav_left:
    if st.button("← Back to Country Snapshot", use_container_width=True):
        st.switch_page('pages/Country_Snapshot.py')
with nav_right:
    if st.button("Compare Countries →", type='primary', use_container_width=True):
        st.switch_page('pages/Country_Comparison.py')
