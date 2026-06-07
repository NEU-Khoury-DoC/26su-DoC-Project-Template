##################################################
# Main entry-point for the Zeus Streamlit app
##################################################

import logging

logging.basicConfig(
    format="%(filename)s:%(lineno)s:%(levelname)s -- %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from modules.zeus_api import get_users

st.set_page_config(layout="wide")

# Returning to Home ends the active persona session and resets the sidebar
st.session_state["authenticated"] = False
st.session_state.pop("role", None)
st.session_state.pop("user_id", None)
st.session_state.pop("first_name", None)

SideBarLinks(show_home=True)

logger.info("Loading the Home page of the app")

st.title("Zeus Energy Security Index")
st.write("Choose a persona, then log in.")

PLACEHOLDER = "Select an option"

PERSONAS = {
    "household_owner_dropdown": ("household_owner", "Household Owner"),
    "journalist_dropdown": ("journalist", "Journalist"),
    "energy_trader_dropdown": ("energy_trader", "Energy Trader"),
}

LOGIN_PAGES = {
    "household_owner": "pages/40_Household_Owner_Dashboard.py",
    "journalist": "pages/Country_Snapshot.py",
    "energy_trader": "pages/Price_Forecast.py",
}


@st.cache_data(ttl=300)
def _cached_users(persona):
    return get_users(persona)


def _persona_users(persona_id):
    try:
        return _cached_users(persona_id)
    except Exception as exc:
        logger.warning("Could not load users for %s: %s", persona_id, exc)
        return []


def _dropdown_options(persona_id):
    users = _persona_users(persona_id)
    names = [user["display_name"] for user in users]
    return [PLACEHOLDER, *names], users


def _persona_option_selected(persona_id: str) -> bool:
    for key, (pid, _) in PERSONAS.items():
        if pid == persona_id:
            return st.session_state.get(key) not in (None, PLACEHOLDER)
    return False


def _on_persona_change(changed_key: str) -> None:
    persona_id, _ = PERSONAS[changed_key]
    selected = st.session_state[changed_key]

    if selected == PLACEHOLDER:
        if st.session_state.get("active_persona") == persona_id:
            st.session_state["active_persona"] = None
        return

    st.session_state["active_persona"] = persona_id
    for key in PERSONAS:
        if key == changed_key:
            continue
        st.session_state[key] = PLACEHOLDER


def _resolve_user(persona_id):
    selected_name = None
    for key, (pid, _) in PERSONAS.items():
        if pid == persona_id:
            selected_name = st.session_state.get(key)
            break
    if not selected_name or selected_name == PLACEHOLDER:
        return None

    for user in _persona_users(persona_id):
        if user["display_name"] == selected_name:
            return user
    return None


if "active_persona" not in st.session_state:
    st.session_state["active_persona"] = None

for key in PERSONAS:
    if key not in st.session_state:
        st.session_state[key] = PLACEHOLDER

active = None
for key, (persona_id, _) in PERSONAS.items():
    if st.session_state.get(key) not in (None, PLACEHOLDER):
        active = persona_id
        break
st.session_state["active_persona"] = active

col_household, col_journalist, col_trader, col_login = st.columns([2, 2, 2, 1])

with col_household:
    _, label = PERSONAS["household_owner_dropdown"]
    options, _ = _dropdown_options("household_owner")
    st.markdown(f"**{label}**")
    st.selectbox(
        f"{label} options",
        options=options,
        key="household_owner_dropdown",
        label_visibility="collapsed",
        on_change=_on_persona_change,
        args=("household_owner_dropdown",),
    )

with col_journalist:
    _, label = PERSONAS["journalist_dropdown"]
    options, _ = _dropdown_options("journalist")
    st.markdown(f"**{label}**")
    st.selectbox(
        f"{label} options",
        options=options,
        key="journalist_dropdown",
        label_visibility="collapsed",
        on_change=_on_persona_change,
        args=("journalist_dropdown",),
    )

with col_trader:
    _, label = PERSONAS["energy_trader_dropdown"]
    options, _ = _dropdown_options("energy_trader")
    st.markdown(f"**{label}**")
    st.selectbox(
        f"{label} options",
        options=options,
        key="energy_trader_dropdown",
        label_visibility="collapsed",
        on_change=_on_persona_change,
        args=("energy_trader_dropdown",),
    )

with col_login:
    st.markdown("&nbsp;", unsafe_allow_html=True)
    if st.button("Log in", type="primary", use_container_width=True):
        persona = st.session_state.get("active_persona")
        if not persona or not _persona_option_selected(persona):
            st.warning("Select a persona and choose an option before logging in.")
        elif persona not in LOGIN_PAGES:
            st.warning("Login for this persona is not available yet.")
        else:
            user = _resolve_user(persona)
            if not user:
                st.error("Could not resolve the selected user. Is the API running?")
            else:
                st.session_state["authenticated"] = True
                st.session_state["role"] = persona
                st.session_state["user_id"] = user["user_id"]
                st.session_state["first_name"] = user.get("first_name") or user["display_name"]
                st.switch_page(LOGIN_PAGES[persona])
