import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide', page_title="Farmers Market")

st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

# hero section
st.markdown("""
<div style='padding: 2rem 0 1rem 0;'>
    <h1 style='font-size: 3rem; margin-bottom: 0.5rem;'>🌾 Farmers Market</h1>
    <p style='font-size: 1.2rem; color: gray;'>
        Data-driven agricultural insights for farmers, policymakers, and researchers across Europe.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# fetch users
def fetch_users_by_role(role):
    try:
        r = requests.get(f"http://web-api:4000/users/{role}", timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        st.error(f"API error: {e}")
        return []

def parse_selected_user(selection):
    user_id_text, user_name = selection.split(': ', 1)
    return int(user_id_text), user_name

farmer_data = fetch_users_by_role('farmer')
farmer_names = [f"{u['user_id']}: {u['user_name']}" for u in farmer_data]

policy_data = fetch_users_by_role('politician')
policy_maker_names = [f"{u['user_id']}: {u['user_name']}" for u in policy_data]

researcher_data = fetch_users_by_role('researcher')
researcher_names = [f"{u['user_id']}: {u['user_name']}" for u in researcher_data]

st.subheader("Sign in")
st.write("Select your profile and role to get started.")

# login cards
farmer_card, policy_card, researcher_card = st.columns(3)

farmer_variable_col, farmer_col = st.columns([3, 2])

with farmer_variable_col:
    st.selectbox(
        'Choose a Farmer',
        farmer_names,
        key='selected_farmer_name',
        label_visibility='collapsed',
        index=None,
        placeholder='Type a name or ID to search…',
    )

with farmer_col:
    if st.button("Log in as Farmer",
                type='primary',
                use_container_width=True,
                key='login_farmer_button'):
        if not st.session_state['selected_farmer_name']:
            st.warning('Please choose a farmer first.')
            st.stop()
        selected_farmer_id, selected_farmer_name = parse_selected_user(
            st.session_state['selected_farmer_name'])
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'farmer'
        st.session_state['first_name'] = selected_farmer_name
        st.session_state['user_id'] = selected_farmer_id
        st.session_state['selected_farmer_id'] = selected_farmer_id
        st.session_state['selected_farmer_display'] = selected_farmer_name
        logger.info("Logging in as Farmer Persona")
        st.switch_page('pages/01_Farmer_Home.py')

policy_variable_col, policy_col = st.columns([3, 2])

with policy_variable_col:
    st.selectbox(
        'Choose a Policy Maker',
        policy_maker_names,
        key='selected_policy_maker_name',
        label_visibility='collapsed',
        index=None,
        placeholder='Type a name or ID to search…',
    )

with policy_col:
    if st.button('Log in as Policy Maker',
                 type='primary',
                 use_container_width=True,
                 key='login_policy_button'):
        if not st.session_state['selected_policy_maker_name']:
            st.warning('Please choose a policy maker first.')
            st.stop()
        selected_policy_id, selected_policy_name = parse_selected_user(
            st.session_state['selected_policy_maker_name'])
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'policy_maker'
        st.session_state['first_name'] = selected_policy_name
        st.session_state['user_id'] = selected_policy_id
        st.session_state['selected_policy_maker_id'] = selected_policy_id
        st.session_state['selected_policy_maker_display'] = selected_policy_name
        st.switch_page('pages/11_Policy_Home.py')


reseacher_variable_col, researcher_col = st.columns([3, 2])

with reseacher_variable_col:
    st.selectbox(
        'Choose a Researcher',
        researcher_names,
        key='selected_researcher_name',
        label_visibility='collapsed',
        index=None,
        placeholder='Type a name or ID to search…',
    )

with researcher_col:
    if st.button('Log in as Researcher',
                type='primary',
                use_container_width=True,
                key='login_researcher_button'):
        if not st.session_state['selected_researcher_name']:
            st.warning('Please choose a researcher first.')
            st.stop()
        selected_researcher_id, selected_researcher_name = parse_selected_user(
            st.session_state['selected_researcher_name'])
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'researcher'
        st.session_state['first_name'] = selected_researcher_name
        st.session_state['user_id'] = selected_researcher_id
        st.session_state['selected_researcher_id'] = selected_researcher_id
        st.session_state['selected_researcher_display'] = selected_researcher_name
        st.switch_page('pages/21_Researcher_Home.py')

st.divider()
# feature highlights
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 👨‍🌾 For Farmers")
    st.write("Predict crop selling prices, log growing conditions, and connect with the agricultural community.")
with col2:
    st.markdown("### 🏛 For Policymakers")
    st.write("Explore regional price maps, compare countries and crops, and generate policy reports.")
with col3:
    st.markdown("### 🔬 For Researchers")
    st.write("Analyse crop observation data, visualise trends, and export datasets for research.")
st.divider()

st.caption("Farmers Market — Built using Eurostat price data and Open-Meteo weather records across 25 EU countries.")