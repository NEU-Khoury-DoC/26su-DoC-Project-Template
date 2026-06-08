import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"RESEARCHER EXPORT")
st.write('Export collected researcher datasets for offline analysis or sharing.')

st.subheader('Export Options')
format = st.selectbox('Format', ['CSV', 'Excel', 'JSON'])
date_from = st.date_input('From')
date_to = st.date_input('To')

if st.button('Prepare Export'):
	# placeholder sample data
	import pandas as pd
	df = pd.DataFrame([{'date':'2024-01-01','crop':'Wheat','value':10}])
	if format == 'CSV':
		st.download_button('Download CSV', df.to_csv(index=False), file_name='data_export.csv')
	elif format == 'Excel':
		st.download_button('Download Excel', df.to_csv(index=False), file_name='data_export.xlsx')
	else:
		st.download_button('Download JSON', df.to_json(orient='records'), file_name='data_export.json')
