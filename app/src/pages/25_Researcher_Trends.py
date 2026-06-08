import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"RESEARCHER TRENDS")
st.write('Explore trends and visualize historic observations for crops and regions.')

col1, col2 = st.columns([3,1])

with col2:
	st.subheader('Controls')
	metric = st.selectbox('Metric', ['temperature', 'humidity', 'rainfall'])
	crop = st.selectbox('Crop', ['All', 'Wheat', 'Maize', 'Rice'])
	if st.button('Update Chart'):
		st.experimental_rerun()

with col1:
	st.subheader('Trend View')
	import pandas as pd
	df = pd.DataFrame({'date': pd.date_range('2024-01-01', periods=12), 'value': range(12)})
	df = df.set_index('date')
	st.line_chart(df)

st.markdown('---')
st.subheader('Aggregated Table')
st.table(pd.DataFrame([{'month':'Jan','avg':20},{'month':'Feb','avg':21}]))