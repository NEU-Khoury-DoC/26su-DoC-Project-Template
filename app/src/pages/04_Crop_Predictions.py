import logging
logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Farmer: Crop Type Predictions")

tab1, tab2 = st.tabs(["Predict", "Saved Predictions"])


# ─────────────────────────────────────────────
# TAB 1 — set a prediction
# ─────────────────────────────────────────────
with tab1:
    st.subheader("Recommend crop to plant")
    st.write("Select available farming resources and environmental conditions.")

    user_id = st.session_state.get('user_id')
    type_of_crop = st.selectbox('Crop Category', ['Root&tuber', 'bulbvegetables', 'cereals', 'colecrops', 'fibre crop', 'millets', 'oil seeds', 'pulses', 'sugar crops', 'vegetables'])
    season_labels = {'Zaid': 'Summer (Zaid)', 'kharif': 'Monsoon (Kharif)', 'rabi': 'Winter (Rabi)'}
    season = st.selectbox('Season', ['Zaid', 'kharif', 'rabi'], format_func=lambda s: season_labels[s])
    water_source = st.selectbox('Water Source', ['irrigated', 'rainfed'])
    sown = st.date_input('Sowing Date')
    harvested = st.date_input('Harvest Date')
    crop_duration = st.slider('Crop Duration (days)', min_value=0, max_value=150, value=100, step=1)
    temperature = st.slider('Average Temperature (°C)', min_value=0.0, max_value=40.0, value=25.0, step=0.5)
    water_required = st.slider('Water Required (mm)', min_value=0, max_value=2500, value=800, step=10)
    relative_humidity = st.slider('Relative Humidity (%)', min_value=0.0, max_value=80.0, value=60.0, step=1.0)
    N = st.slider('Soil Nitrogen (N)', min_value=0.0, max_value=100.0, value=50.0, step=1.0)
    P = st.slider('Soil Phosphorus (P)', min_value=0.0, max_value=60.0, value=30.0, step=1.0)
    K = st.slider('Soil Potassium (K)', min_value=0.0, max_value=60.0, value=30.0, step=1.0)

    if st.button('Predict'):
        logger.info(f'Prediction request- crop category: {type_of_crop}, season: {season}')
        # model only wants the month abbrev (e.g. 'Jun'); we keep the full dates for saving
        sown_month = sown.strftime('%B')[:3]
        harvested_month = harvested.strftime('%B')[:3]
        try:
            response = requests.get(
                f'http://web-api:4000/crop/model3/prediction/{N}/{P}/{K}/{type_of_crop}/{temperature}/{season}/{sown_month}/{harvested_month}/{water_source}/{relative_humidity}/{crop_duration}/{water_required}'
            )
            response.raise_for_status()
            result = response.json()
            preds = result['predictions']

            st.session_state['last_pred']={
                "farmer_id": user_id,          
                "type_of_crop": type_of_crop,
                "sown": sown.isoformat(),
                "harvested": harvested.isoformat(),
                "water_source": water_source,
                "predicted_crop": preds[0],        
            } #save pred

            st.success('Prediction complete!')
            m1, m2 = st.columns(2)
            with m1:
                st.metric(label='Crop Category', value=type_of_crop)
            with m2:
                st.metric(label='Season', value=season)

            st.write('### Recommended crops (most likely first)')
            for rank, crop in enumerate(preds, start=1):
                st.write(f'{rank}. {crop}')


        except Exception as e:
            logger.error(f'Prediction error: {e}')
            st.error(f'Could not retrieve prediction: {e}')

    if 'last_pred' in st.session_state:
        if st.button("Save Prediction"):
            r=requests.post('http://web-api:4000/pred/pred',json=st.session_state['last_pred'])
            if r.status_code==201:
                st.success("Saved!")
            else:
                st.error(f"Save failed: {r.text}")


# ─────────────────────────────────────────────
# TAB 2 — view past predictions
# ─────────────────────────────────────────────
with tab2:
    st.subheader("View saved predictions")

    user_id = st.session_state.get('user_id')
    try:
        r = requests.get('http://web-api:4000/pred/pastpreds')
        r.raise_for_status()
        rows = r.json()

        # keep only the logged-in farmer's saved predictions
        if user_id is not None:
            rows = [row for row in rows if row.get('farmer_id') == user_id]

        if rows:
            st.dataframe(rows, use_container_width=True)
        else:
            st.info("No saved predictions yet. Make a prediction in the first tab and click Save.")
    except Exception as e:
        st.error(f"Could not load saved predictions: {e}")