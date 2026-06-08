import logging
logger = logging.getLogger(__name__)

import plotly.express as px
import streamlit as st
from modules.nav import SideBarLinks
from modules.theme import zeus_plotly_layout
from modules.trader_data import (
    BIDDING_ZONES, ZONE_NAMES, fetch_forecast, forecast_summary,
)

st.set_page_config(layout='wide')

SideBarLinks()

st.title("30-Day Price Forecast")

default_country = st.session_state.get("trader_country", "Germany")
selected_country = st.selectbox(
    "Select Market",
    ZONE_NAMES,
    index=ZONE_NAMES.index(default_country) if default_country in ZONE_NAMES else 0,
)
st.session_state["trader_country"] = selected_country
code = BIDDING_ZONES[selected_country]

forecast, is_live = fetch_forecast(code)
s = forecast_summary(forecast)

if not is_live:
    st.warning(
        "**Showing an illustrative forecast.** The live price-forecast API "
        "is not returning data right now, so the numbers below are placeholder "
        "values to preview the page layout. Once the ML1 endpoint is serving "
        "predictions, this page will show the real 30-day path."
    )

st.divider()

st.subheader(f"{selected_country} — next 30 days")

m1, m2, m3 = st.columns(3)
m1.metric("Forecast start (day 1)", f"€{s['day1']:.1f}/MWh")
m2.metric(
    "Forecast end (day 30)",
    f"€{s['day30']:.1f}/MWh",
    f"{s['trend_pct']:+.1f}% over the month",
)
m3.metric("Expected range", f"€{s['min']:.0f} – €{s['max']:.0f}")

st.divider()

st.write(f"##### Projected day-ahead price path for {selected_country}")

fig = px.line(
    forecast, x="date", y="predicted_price_eur_mwh",
    labels={"date": "", "predicted_price_eur_mwh": "Price €/MWh"},
)
fig.add_hline(
    y=s["avg"], line_dash="dash", line_color="gray",
    annotation_text=f"30-day avg €{s['avg']:.0f}",
)
zeus_plotly_layout(fig, height=400)
st.plotly_chart(fig, use_container_width=True)
st.caption(
    "The model rolls each day's prediction forward as an input to the next, "
    "so treat the far end of the curve as a trend, not a point estimate."
)

st.divider()

st.write("##### Trading signals")

trend_pct = s["trend_pct"]
if trend_pct > 5:
    st.warning(
        f"**Upward trend ({trend_pct:+.1f}%).** The curve is climbing. If you "
        "are short forward or carry consumption exposure, this is the window to "
        "lock in or layer hedges before the move materialises. Watch for the "
        "rally being driven by fuel costs or a cold/low-wind snap — those "
        "reverse faster than structural demand shifts."
    )
elif trend_pct < -5:
    st.info(
        f"**Downward trend ({trend_pct:+.1f}%).** The model sees prices easing. "
        "Hedgers can wait rather than chase forwards; length looks expensive "
        "into the weakness. Confirm the softness against the gas curve and the "
        "renewables outlook before sizing any short."
    )
else:
    st.success(
        f"**Range-bound ({trend_pct:+.1f}%).** No strong directional edge over "
        f"the month. The opportunity is in the €{s['min']:.0f}–€{s['max']:.0f} "
        "oscillation — mean-reversion and intraday spreads over outright "
        "directional bets. Keep hedges rolling on schedule."
    )

st.write(
    "Forecasts are decision support, not execution instructions. Size against "
    "your risk limits and confirm the signal against live fuels, weather, and "
    "cross-border flows before you trade."
)

st.write("")
left, right = st.columns(2)

with left:
    st.write("**Watch these intraday**")
    st.markdown(
        "- [EPEX SPOT](https://www.epexspot.com) — day-ahead and intraday "
        "auctions for Central/Western Europe\n"
        "- [Nord Pool](https://www.nordpoolgroup.com) — day-ahead clearing "
        "prices across the Nordic and Baltic zones\n"
        "- [ENTSO-E Transparency](https://transparency.entsoe.eu) — load, "
        "generation and cross-border flows that move price"
    )

with right:
    st.write("**Context for the curve**")
    st.markdown(
        "- [EEX](https://www.eex.com) — power, gas and emissions futures that "
        "anchor the forward curve\n"
        "- [TTF gas](https://www.theice.com) — the marginal fuel for much of "
        "EU power; gas leads, power follows\n"
        "- [ENTSO-E forecasts](https://www.entsoe.eu) — wind/solar outlooks "
        "that drive the volatility band above"
    )

st.divider()

nav_left, nav_right = st.columns(2)
with nav_left:
    if st.button("My Markets →", type="primary", use_container_width=True):
        st.switch_page("pages/My_Markets.py")
with nav_right:
    if st.button("Trade Journal →", use_container_width=True):
        st.switch_page("pages/Trade_Journal.py")
