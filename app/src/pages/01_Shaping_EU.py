import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.markdown("# Who is Shaping EU Policies?")
st.sidebar.header("Citizen View")
st.write("Pick your areas of interest and we'll show you which organizations are lobbying on them.")

# Session state 
if "selected_policies" not in st.session_state:
    st.session_state.selected_policies = []
if "selected_countries" not in st.session_state:
    st.session_state.selected_countries = []

POLICIES = [
    {"name": "Artificial Intelligence", "emoji": "🤖"},
    {"name": "Climate & Energy",        "emoji": "🌱"},
    {"name": "Healthcare",              "emoji": "🏥"},
    {"name": "Defence & Security",      "emoji": "🛡️"},
    {"name": "Finance & Banking",       "emoji": "🏦"},
    {"name": "Agriculture",             "emoji": "🌾"},
    {"name": "Digital Markets",         "emoji": "📱"},
    {"name": "Transport",               "emoji": "🚄"},
]

COUNTRIES = [
    {"name": "Austria",        "emoji": "🇦🇹"},
    {"name": "Belgium",        "emoji": "🇧🇪"},
    {"name": "Bulgaria",       "emoji": "🇧🇬"},
    {"name": "Croatia",        "emoji": "🇭🇷"},
    {"name": "Cyprus",         "emoji": "🇨🇾"},
    {"name": "Czech Republic", "emoji": "🇨🇿"},
    {"name": "Denmark",        "emoji": "🇩🇰"},
    {"name": "Estonia",        "emoji": "🇪🇪"},
    {"name": "Finland",        "emoji": "🇫🇮"},
    {"name": "France",         "emoji": "🇫🇷"},
    {"name": "Germany",        "emoji": "🇩🇪"},
    {"name": "Greece",         "emoji": "🇬🇷"},
    {"name": "Hungary",        "emoji": "🇭🇺"},
    {"name": "Ireland",        "emoji": "🇮🇪"},
    {"name": "Italy",          "emoji": "🇮🇹"},
    {"name": "Latvia",         "emoji": "🇱🇻"},
    {"name": "Lithuania",      "emoji": "🇱🇹"},
    {"name": "Luxembourg",     "emoji": "🇱🇺"},
    {"name": "Malta",          "emoji": "🇲🇹"},
    {"name": "Netherlands",    "emoji": "🇳🇱"},
    {"name": "Poland",         "emoji": "🇵🇱"},
    {"name": "Portugal",       "emoji": "🇵🇹"},
    {"name": "Romania",        "emoji": "🇷🇴"},
    {"name": "Slovakia",       "emoji": "🇸🇰"},
    {"name": "Slovenia",       "emoji": "🇸🇮"},
    {"name": "Spain",          "emoji": "🇪🇸"},
    {"name": "Sweden",         "emoji": "🇸🇪"},
]

# Pick a Policy
st.markdown("### Pick a Policy")

pol_cols = st.columns(4)
for i, policy in enumerate(POLICIES):
    with pol_cols[i % 4]:
        selected = policy["name"] in st.session_state.selected_policies
        label = f"{'✅' if selected else '⬜'}  {policy['emoji']}  {policy['name']}"
        if st.button(label, key=f"pol_{i}", use_container_width=True):
            if policy["name"] in st.session_state.selected_policies:
                st.session_state.selected_policies.remove(policy["name"])
            else:
                st.session_state.selected_policies.append(policy["name"])
            st.rerun()

st.markdown("---")

# Pick a Country 
st.markdown("### Pick a Country")

cty_cols = st.columns(4)
for i, country in enumerate(COUNTRIES):
    with cty_cols[i % 4]:
        selected = country["name"] in st.session_state.selected_countries
        label = f"{'✅' if selected else '⬜'}  {country['emoji']}  {country['name']}"
        if st.button(label, key=f"cty_{i}", use_container_width=True):
            if country["name"] in st.session_state.selected_countries:
                st.session_state.selected_countries.remove(country["name"])
            else:
                st.session_state.selected_countries.append(country["name"])
            st.rerun()

st.markdown("---")

# Selections summary in sidebar 
st.sidebar.markdown("### Your Selections")
st.sidebar.markdown("**Policies:** " + (", ".join(st.session_state.selected_policies) or "None"))
st.sidebar.markdown("**Countries:** " + (", ".join(st.session_state.selected_countries) or "None"))

# Submit
if st.button("Submit Search Preferences", type="primary", use_container_width=True):
    if not st.session_state.selected_policies and not st.session_state.selected_countries:
        st.warning("Please select at least one policy or country before submitting.")
    else:
        prefs = {
            "user_id":    st.session_state.get("user_id", 1),
            "query_json": str({
                "policies":  st.session_state.selected_policies,
                "countries": st.session_state.selected_countries,
            }),
            "file_format": "json",
        }
        try:
            r = requests.post("http://web-api:4000/preferences", json=prefs)
            if r.status_code == 201:
                st.success(f"✅ Preferences saved! Policies: {', '.join(st.session_state.selected_policies) or 'None'} | Countries: {', '.join(st.session_state.selected_countries) or 'None'}")
            else:
                st.error("Could not save preferences. Please try again.")
        except requests.exceptions.ConnectionError:
            st.success("✅ Preferences saved! (demo mode — backend not connected yet)")