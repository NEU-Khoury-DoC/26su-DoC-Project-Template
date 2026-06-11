import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import plotly.express as px
import requests

from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title("Crop Price Map")
st.write("Explore historical and predicted crop prices across Europe.")

API_BASE = "http://web-api:4000"

CROPS = ['Barley', 'Durum wheat', 'Feed barley', 'Rye', 'Soft wheat']
COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia',
             'Denmark', 'Estonia', 'Finland', 'Germany', 'Greece', 'Hungary',
             'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
             'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia',
             'Slovenia', 'Spain', 'Sweden']

# cache predictions for 1 hour so we dont call the model 25 times on every load
@st.cache_data(ttl=3600)
def get_all_predictions(crop):
    results = []
    for country in COUNTRIES:
        try:
            r = requests.get(
                f"{API_BASE}/prices_model/prediction/{crop}/{country}",
                timeout=10
            )
            if r.status_code == 200:
                results.append({
                    'country': country,
                    'predicted_price': round(r.json()['prediction'], 2)
                })
        except:
            pass
    return pd.DataFrame(results)

tab1, tab2 = st.tabs(["Historical prices", "Predicted prices"])

with tab1:
    st.subheader("Average historical selling price by country")

    col1, col2 = st.columns(2)
    with col1:
        crop_filter = st.selectbox("Filter by crop", ["All crops"] + CROPS, key="hist_crop")
    with col2:
        year_range = st.slider("Year range", 2017, 2024, (2017, 2024))

    try:
        response = requests.get(f"{API_BASE}/prices_model/average", params={
            'year_min': year_range[0],
            'year_max': year_range[1]
        })
        data = response.json()
        df = pd.DataFrame(data)

        df['avg_price'] = pd.to_numeric(df['avg_price'], errors='coerce')
        
        if crop_filter != "All crops":
            df = df[df['prod_veg'] == crop_filter]

        df_map = df.groupby('geo')['avg_price'].mean().reset_index()
        df_map.columns = ['country', 'avg_price']

        fig = px.choropleth(
            df_map,
            locations='country',
            locationmode='country names',
            color='avg_price',
            scope='europe',
            color_continuous_scale='YlOrRd',
            title=f'Average selling price {year_range[0]}–{year_range[1]} — {crop_filter}',
            labels={'avg_price': '€ / 100kg'}
        )
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)

        st.caption("\* France and Malta are excluded as crop price data is not available.")

        with st.expander("View data table"):
            st.dataframe(df_map.sort_values('avg_price', ascending=False), use_container_width=True)

    except Exception as e:
        st.error(f"Could not load historical data: {e}")

with tab2:
    st.subheader("Predicted selling price by country")
    st.write("Based on the linear regression model using weather data and recent price history.")

    pred_crop = st.selectbox("Select crop", CROPS, key="pred_crop")

    with st.spinner("Loading predictions..."):
        df_pred = get_all_predictions(pred_crop)

    if not df_pred.empty:
        fig2 = px.choropleth(
            df_pred,
            locations='country',
            locationmode='country names',
            color='predicted_price',
            scope='europe',
            color_continuous_scale='YlOrRd',
            title=f'Predicted price — {pred_crop}',
            labels={'predicted_price': '€ / 100kg'}
        )
        fig2.update_layout(margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig2, use_container_width=True)

        st.caption("\* France and Malta are excluded as crop price data is not available.")

        with st.expander("View data table"):
            st.dataframe(df_pred.sort_values('predicted_price', ascending=False), use_container_width=True)
    else:
        st.error("Could not load predictions.")
