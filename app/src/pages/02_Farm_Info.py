import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Insert Farm Information")
st.write('Place for farmers to input their information about their farm')

text_input = st.text_input("Enter some text", placeholder="Type something...")
dropdown = st.selectbox("Choose an option", ["Option A", "Option B", "Option C"])
 
# Submit button
if st.button("Submit"):
    # --- Your backend logic goes here ---
    result = handle_submission(text_input, dropdown)
    st.success(f"Submitted! Text: '{text_input}', Option: '{dropdown}'")
    st.write("Backend response:", result)
 
 
def handle_submission(text: str, option: str) -> dict:
    """Replace this with your actual backend logic."""
    return {"received_text": text, "received_option": option}
 