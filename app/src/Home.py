##################################################
# This is the main/entry-point file for the
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

import requests

# streamlit supports regular and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout='wide')

# If a user is at this page, we assume they are not
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false.
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel.
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

logger.info("Loading the Home page of the app")
st.title('Welcome to Farmers Market')
st.write('#### Hi! As which user would you like to log in?')

##THESE ARE ALL PLACEHOLDERS UNTIL API IS MADE

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


# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user
# can click to MIMIC logging in as that mock user.


farmer_variable_col, farmer_col = st.columns([3, 2])

with farmer_variable_col:
    st.selectbox(
        'Choose a Farmer',
        farmer_names,
        key='selected_farmer_name',
        label_visibility='collapsed',
    )

with farmer_col:
    if st.button("Log In as Farmer",
                type='primary',
                use_container_width=True,
                key='login_farmer_button'):
        selected_farmer_id, selected_farmer_name = parse_selected_user(
            st.session_state['selected_farmer_name']
        )
        # when user clicks the button, they are now considered authenticated
        st.session_state['authenticated'] = True
        # we set the role of the current user
        st.session_state['role'] = 'farmer'
        # we add the first name of the user (so it can be displayed on
        # subsequent pages).
        st.session_state['first_name'] = selected_farmer_name
        st.session_state['user_id'] = selected_farmer_id
        st.session_state['selected_farmer_id'] = selected_farmer_id
        st.session_state['selected_farmer_display'] = selected_farmer_name
        # finally, we ask streamlit to switch to another page, in this case, the
        # landing page for this particular user type
        logger.info("Logging in as Farmer Persona")
        st.switch_page('pages/01_Farmer_Home.py')

policy_variable_col, policy_col = st.columns([3, 2])

with policy_variable_col:
    st.selectbox(
        'Choose a Policy Maker',
        policy_maker_names,
        key='selected_policy_maker_name',
        label_visibility='collapsed',
    )

with policy_col:
    if st.button('Log in as Policy Maker',
                 type='primary',
                 use_container_width=True,
                 key='login_policy_button'):
        selected_policy_id, selected_policy_name = parse_selected_user(
            st.session_state['selected_policy_maker_name']
        )
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
    )

with researcher_col:
    if st.button('Log in as Researcher',
                type='primary',
                use_container_width=True,
                key='login_researcher_button'):
        selected_researcher_id, selected_researcher_name = parse_selected_user(
            st.session_state['selected_researcher_name']
        )
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'researcher'
        st.session_state['first_name'] = selected_researcher_name
        st.session_state['user_id'] = selected_researcher_id
        st.session_state['selected_researcher_id'] = selected_researcher_id
        st.session_state['selected_researcher_display'] = selected_researcher_name
        st.switch_page('pages/21_Researcher_Home.py')
