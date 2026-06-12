import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Crop Price Prediction")
st.write("Predict the next selling price for a crop in a specific country.")

CROPS = ['Barley', 'Durum wheat', 'Feed barley', 'Rye', 'Soft wheat']
COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia',
             'Denmark', 'Estonia', 'Finland', 'Germany', 'Greece', 'Hungary',
             'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
             'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia',
             'Slovenia', 'Spain', 'Sweden']

crop = st.selectbox('Crop', CROPS, index=CROPS.index('Durum wheat'))
region = st.selectbox('Country / Region', COUNTRIES)
st.caption("\* France and Malta are excluded as crop price data is not available.")

if st.button('Predict'):
    logger.info(f'Prediction — crop: {crop}, region: {region}')
    try:
        response = requests.get(
            f'http://web-api:4000/prices_model/prediction/{crop}/{region}'
        )
        if response.status_code == 400:
            error = response.json().get('error', '')
            if 'Not enough price history' in error:
                st.warning(f"No price data available for {crop} in {region}. Try a different combination.")
            else:
                st.error(f"Could not make prediction: {error}")
        elif response.status_code == 200:
            pred = response.json()['prediction']

            # get historical prices for this crop/country
            hist_response = requests.get(f"http://web-api:4000/prices_model/average", params={
                'year_min': 2017, 'year_max': 2024
            })
            hist_data = pd.DataFrame(hist_response.json())
            
            hist_data['avg_price'] = pd.to_numeric(hist_data['avg_price'], errors='coerce')
            hist_filtered = hist_data[
                (hist_data['geo'] == region) & (hist_data['prod_veg'] == crop)
            ].copy()

            # metrics row
            historical_avg = hist_filtered['avg_price'].mean()
            pct_diff = ((pred - historical_avg) / historical_avg) * 100
            direction = "above" if pct_diff > 0 else "below"

            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Predicted price", f"€{pred:,.2f}")
            with m2:
                st.metric("Historical average", f"€{historical_avg:,.2f}")
            with m3:
                st.metric("vs historical avg", f"{abs(pct_diff):.1f}% {direction}",
                         delta=f"{pct_diff:.1f}%")
                
            st.caption("Prices are in € per 100kg. Multiply by 10 for price per tonne.")

            # context sentence
            if abs(pct_diff) < 5:
                context = f"The predicted price for **{crop}** in **{region}** is in line with the historical average."
            elif pct_diff > 0:
                context = f"The predicted price for **{crop}** in **{region}** is **{pct_diff:.1f}% above** the 2017–2024 average, suggesting above-normal market conditions."
            else:
                context = f"The predicted price for **{crop}** in **{region}** is **{abs(pct_diff):.1f}% below** the 2017–2024 average, suggesting favourable supply conditions."
            st.info(context)

            # trend line with prediction as next point
            if not hist_filtered.empty:
                # get per-year prices from CropPrices directly
                all_hist_response = requests.get(f"http://web-api:4000/prices_model/average", params={
                    'year_min': 2017, 'year_max': 2024
                })
                # use the average route per year by fetching each year
                years = list(range(2017, 2025))
                yearly_prices = []
                for year in years:
                    r = requests.get(f"http://web-api:4000/prices_model/average", params={
                        'year_min': year, 'year_max': year
                    })
                    if r.status_code == 200:
                        year_data = pd.DataFrame(r.json())
                        year_data['avg_price'] = pd.to_numeric(year_data['avg_price'], errors='coerce')
                        match = year_data[
                            (year_data['geo'] == region) & (year_data['prod_veg'] == crop)
                        ]
                        if not match.empty:
                            yearly_prices.append({'year': year, 'price': match['avg_price'].iloc[0], 'type': 'Historical'})

                yearly_prices.append({'year': 2025, 'price': pred, 'type': 'Predicted'})
                trend_df = pd.DataFrame(yearly_prices)

                fig = go.Figure()
                hist_df = trend_df[trend_df['type'] == 'Historical']
                pred_df = trend_df[trend_df['type'] == 'Predicted']

                fig.add_trace(go.Scatter(
                    x=hist_df['year'], y=hist_df['price'],
                    mode='lines+markers', name='Historical',
                    line=dict(color='steelblue', width=2),
                    marker=dict(size=6)
                ))
                fig.add_trace(go.Scatter(
                    x=[hist_df['year'].iloc[-1], pred_df['year'].iloc[0]],
                    y=[hist_df['price'].iloc[-1], pred_df['price'].iloc[0]],
                    mode='lines', showlegend=False,
                    line=dict(color='tomato', width=2, dash='dash')
                ))
                fig.add_trace(go.Scatter(
                    x=pred_df['year'], y=pred_df['price'],
                    mode='markers', name='Predicted',
                    marker=dict(size=10, color='tomato', symbol='star')
                ))
                fig.update_layout(
                    title=f'{crop} price in {region} — historical and predicted',
                    xaxis_title='Year',
                    yaxis_title='€ / 100kg',
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        logger.error(f'Prediction error: {e}')
        st.error(f'Could not retrieve prediction: {e}')