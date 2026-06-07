import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"RESEARCHER REPROT")
st.write('Generate summary reports from collected observations. Choose filters and export a PDF/summary.')

col1, col2 = st.columns([3,1])

with col2:
	st.subheader('Report Options')
	report_type = st.selectbox('Report type', ['Summary', 'Temporal Analysis', 'Export for Stakeholders'])
	include_maps = st.checkbox('Include maps', value=True)
	if st.button('Generate Report'):
		st.info('Report generation started (placeholder)')

with col1:
	st.subheader('Preview')
	st.write('Report preview will be rendered here once generated. This is a placeholder.')
