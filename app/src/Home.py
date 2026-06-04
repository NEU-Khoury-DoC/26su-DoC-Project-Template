##################################################
# This is the main/entry-point file for the
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
import requests
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

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
st.title('Housing Homies App')
st.write('#### Hi! As which user would you like to log in?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user
# can click to MIMIC logging in as that mock user.

#retrieve full list of students
response_students = requests.get('http://web-api:4000/housing/user', params={'role': 'Student'})
students = response_students.json()

#dropdown menu
student_options = {f"{s['name']}": s for s in students}
selected_name_student = st.selectbox('Select a user', options=list(student_options.keys()))

if st.button("Login as a Student",
             type='primary',
             use_container_width=True):
    
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'Student'

    st.session_state['name'] = student_options[selected_name_student]['name']
    st.session_state['user_id'] = student_options[selected_name_student]['user_id']
    logger.info("Logging in as Student Persona")
    st.switch_page('pages/00_Pol_Strat_Home.py')

#retrieve full list of real estate agents
response_agents_re = requests.get('http://web-api:4000/housing/user', 
                                  params={'role': 'Real Estate Agent'})
re_agents = response_agents_re.json()

#dropdown menu
agent_options_re = {f"{a['name']}": a for a in re_agents}
selected_name_agent_re = st.selectbox('Select a user', options=list(agent_options_re.keys()))

if st.button('Login as a Real Estate Agent',
             type='primary',
             use_container_width=True):

    #first_name = response from dropdown menu
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'Real Estate Agent'
    st.session_state['name'] = agent_options_re[selected_name_agent_re]['name']
    st.session_state['user_id'] = agent_options_re[selected_name_agent_re]['user_id']
    st.switch_page('pages/10_USAID_Worker_Home.py')

#retrieve full list of real estate agents
response_ga = requests.get('http://web-api:4000/housing/user', params={'role': 'Government Agency'})
agents_ga = response_ga.json()

#dropdown menu
agent_options_ga = {f"{a['name']}": a for a in agents_ga}
selected_name_ga = st.selectbox('Select a user', options=list(agent_options_ga.keys()))

if st.button('Login as a government agency worker',
             type='primary',
             use_container_width=True):

    #first_name = response from dropdown menu
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'Government Agency'
    st.session_state['name'] = agent_options_ga[selected_name_ga]['name']
    st.session_state['user_id'] = agent_options_ga[selected_name_ga]['user_id']
    st.switch_page('pages/20_Admin_Home.py')
