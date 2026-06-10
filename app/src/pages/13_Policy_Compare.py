import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Compare")
st.write("Compare crop prices across countries, crops, or time periods.")

CROPS = ['Barley', 'Durum wheat', 'Feed barley', 'Rye', 'Soft wheat']
COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia',
             'Denmark', 'Estonia', 'Finland', 'Germany', 'Greece', 'Hungary',
             'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
             'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia',
             'Slovenia', 'Spain', 'Sweden']
PERIODS = ['2017-2019', '2020-2022', '2023-2024']

OPTIONS_MAP = {
    'Country': COUNTRIES,
    'Crop': CROPS,
    'Time period': PERIODS
}

try:
    response = requests.get(f"{API_BASE}/prices_model/average", params={
        'year_min': 2017, 'year_max': 2024
    })
    data = response.json()
    df = pd.DataFrame(data)
    df['avg_price'] = pd.to_numeric(df['avg_price'], errors='coerce')
except:
    st.error("Could not load price data")
    st.stop()

st.subheader("Compare settings")
col_a, col_b, col_c = st.columns(3)

with col_a:
    compare_by = st.selectbox("Compare by", list(OPTIONS_MAP.keys()))
with col_b:
    option_a = st.selectbox("Option A", OPTIONS_MAP[compare_by], key="opt_a")
with col_c:
    remaining = [o for o in OPTIONS_MAP[compare_by] if o != option_a]
    option_b = st.selectbox("Option B", remaining, key="opt_b")

st.divider()

def filter_data(df, compare_by, value):
    if compare_by == 'Country':
        return df[df['geo'] == value]
    elif compare_by == 'Crop':
        return df[df['prod_veg'] == value]
    elif compare_by == 'Time period':
        year_ranges = {
            '2017-2019': (2017, 2019),
            '2020-2022': (2020, 2022),
            '2023-2024': (2023, 2024)
        }
        start, end = year_ranges[value]
        try:
            r = requests.get(f"{API_BASE}/prices_model/average", params={
                'year_min': start, 'year_max': end
            })
            d = pd.DataFrame(r.json())
            d['avg_price'] = pd.to_numeric(d['avg_price'], errors='coerce')
            return d
        except:
            return pd.DataFrame()
    return df

def render_col(col, data, label, compare_by):
    with col:
        st.subheader(label)

        if data.empty:
            st.info("No data available.")
            return

        if compare_by == 'Country':
            fig = px.bar(data, x='prod_veg', y='avg_price',
                title=f'Avg price by crop — {label}',
                labels={'prod_veg': 'Crop', 'avg_price': '€ / 100kg'},
                color='prod_veg')
        elif compare_by == 'Crop':
            fig = px.bar(data, x='geo', y='avg_price',
                title=f'Avg price by country — {label}',
                labels={'geo': 'Country', 'avg_price': '€ / 100kg'},
                color='geo')
        else:
            fig = px.bar(data.groupby('prod_veg')['avg_price'].mean().reset_index(),
                x='prod_veg', y='avg_price',
                title=f'Avg price by crop — {label}',
                labels={'prod_veg': 'Crop', 'avg_price': '€ / 100kg'},
                color='prod_veg')

        fig.update_layout(showlegend=False, xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

        st.metric("Overall avg price", f"€{data['avg_price'].mean():.2f}")
        st.metric("Highest price",
                  f"€{data['avg_price'].max():.2f} — {data.loc[data['avg_price'].idxmax(), 'prod_veg'] if compare_by == 'Country' else data.loc[data['avg_price'].idxmax(), 'geo']}")
        st.metric("Lowest price",
                  f"€{data['avg_price'].min():.2f} — {data.loc[data['avg_price'].idxmin(), 'prod_veg'] if compare_by == 'Country' else data.loc[data['avg_price'].idxmin(), 'geo']}")

def get_predictions(compare_by, value):
    results = []
    if compare_by == 'Country':
        for crop in CROPS:
            try:
                r = requests.get(f"{API_BASE}/prices_model/prediction/{crop}/{value}", timeout=10)
                if r.status_code == 200:
                    results.append({'crop': crop, 'predicted_price': round(r.json()['prediction'], 2)})
            except:
                pass
    elif compare_by == 'Crop':
        for country in COUNTRIES:
            try:
                r = requests.get(f"{API_BASE}/prices_model/prediction/{value}/{country}", timeout=10)
                if r.status_code == 200:
                    results.append({'country': country, 'predicted_price': round(r.json()['prediction'], 2)})
            except:
                pass
    return pd.DataFrame(results)

df_a = filter_data(df, compare_by, option_a)
df_b = filter_data(df, compare_by, option_b)

tab_hist, tab_pred = st.tabs(["Historical prices", "Predicted prices"])

with tab_hist:
    left, right = st.columns(2)
    render_col(left, df_a, option_a, compare_by)
    render_col(right, df_b, option_b, compare_by)

with tab_pred:
    if compare_by in ['Country', 'Crop']:
        pred_col1, pred_col2 = st.columns(2)

        with pred_col1:
            with st.spinner(f"Loading predictions for {option_a}..."):
                pred_a = get_predictions(compare_by, option_a)
            if not pred_a.empty:
                x_col = 'crop' if compare_by == 'Country' else 'country'
                fig = px.bar(pred_a, x=x_col, y='predicted_price',
                    title=f'Predicted prices — {option_a}',
                    labels={x_col: x_col.title(), 'predicted_price': '€ / 100kg'},
                    color=x_col)
                fig.update_layout(showlegend=False, xaxis_tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

        with pred_col2:
            with st.spinner(f"Loading predictions for {option_b}..."):
                pred_b = get_predictions(compare_by, option_b)
            if not pred_b.empty:
                x_col = 'crop' if compare_by == 'Country' else 'country'
                fig = px.bar(pred_b, x=x_col, y='predicted_price',
                    title=f'Predicted prices — {option_b}',
                    labels={x_col: x_col.title(), 'predicted_price': '€ / 100kg'},
                    color=x_col)
                fig.update_layout(showlegend=False, xaxis_tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Predicted price comparison is not available for time period comparisons.")