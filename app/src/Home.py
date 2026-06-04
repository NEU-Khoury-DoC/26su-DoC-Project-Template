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

st.set_page_config(layout="wide")

# Returning to Home ends the active persona session and resets the sidebar
st.session_state["authenticated"] = False
st.session_state.pop("role", None)

SideBarLinks(show_home=True)

logger.info("Loading the Home page of the app")

st.title("Zeus Energy Security Index")
st.write("Choose a persona, then log in.")

PLACEHOLDER = "Select an option"

PERSONAS = {
    "household_owner_dropdown": ("household_owner", "Household Owner", "Option 1"),
    "journalist_dropdown": ("journalist", "Journalist", "Option 1"),
    "analyst_dropdown": ("analyst", "Analyst", "Option 1"),
}

LOGIN_PAGES = {
    "household_owner": "pages/40_Household_Owner_Dashboard.py",
    "journalist": "pages/Country_Snapshot.py",
}


def _persona_option_selected(persona_id: str) -> bool:
    """True only when the persona's dropdown has a real option, not the placeholder."""
    for key, (pid, _, option) in PERSONAS.items():
        if pid == persona_id:
            return st.session_state.get(key) == option
    return False


def _on_persona_change(changed_key: str) -> None:
    """Keep a single active persona across the three dropdowns."""
    persona_id, _, _ = PERSONAS[changed_key]
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


if "active_persona" not in st.session_state:
    st.session_state["active_persona"] = None

for key in PERSONAS:
    if key not in st.session_state:
        st.session_state[key] = PLACEHOLDER

# Keep active_persona in sync so login never uses a stale persona with placeholders
active = None
for key, (persona_id, _, option) in PERSONAS.items():
    if st.session_state.get(key) == option:
        active = persona_id
        break
st.session_state["active_persona"] = active

col_household, col_journalist, col_analyst, col_login = st.columns([2, 2, 2, 1])

with col_household:
    _, label, option = PERSONAS["household_owner_dropdown"]
    st.markdown(f"**{label}**")
    st.selectbox(
        f"{label} options",
        options=[PLACEHOLDER, option],
        key="household_owner_dropdown",
        label_visibility="collapsed",
        on_change=_on_persona_change,
        args=("household_owner_dropdown",),
    )

with col_journalist:
    _, label, option = PERSONAS["journalist_dropdown"]
    st.markdown(f"**{label}**")
    st.selectbox(
        f"{label} options",
        options=[PLACEHOLDER, option],
        key="journalist_dropdown",
        label_visibility="collapsed",
        on_change=_on_persona_change,
        args=("journalist_dropdown",),
    )

with col_analyst:
    _, label, option = PERSONAS["analyst_dropdown"]
    st.markdown(f"**{label}**")
    st.selectbox(
        f"{label} options",
        options=[PLACEHOLDER, option],
        key="analyst_dropdown",
        label_visibility="collapsed",
        on_change=_on_persona_change,
        args=("analyst_dropdown",),
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
            st.session_state["authenticated"] = True
            st.session_state["role"] = persona
            st.switch_page(LOGIN_PAGES[persona])
