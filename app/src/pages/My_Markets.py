import logging
logger = logging.getLogger(__name__)

import pandas as pd
import plotly.express as px
import streamlit as st
from modules.nav import SideBarLinks
from modules.theme import zeus_plotly_layout
from modules.trader_data import (
    BIDDING_ZONES, CODE_TO_NAME, ZONE_NAMES,
    fetch_forecast, forecast_summary,
)

st.set_page_config(layout="wide")

SideBarLinks()

trader = st.session_state.get("first_name", "Trader")

st.title("My Markets")
st.write("#### The zones you're trading — the 30-day forecast, side by side")
st.write(
    f"{trader}, this is your scoped view: only the bidding zones on your "
    "watchlist, each showing the 30-day price direction. Set a threshold and "
    "the desk flags the zone for you so you don't have to recheck it all day."
)

# ---- Watchlist (story 1) ----------------------------------------------------
# Persisted in session for this demo; a production build would store the
# watchlist per user in the database.
if "trader_watchlist" not in st.session_state:
    st.session_state["trader_watchlist"] = ["NL", "DE"]  # Niels trades from Amsterdam
if "trader_alerts" not in st.session_state:
    st.session_state["trader_alerts"] = {}  # code -> {"threshold": float, "direction": str}

current_names = [CODE_TO_NAME[c] for c in st.session_state["trader_watchlist"]
                 if c in CODE_TO_NAME]

st.divider()
st.write("##### Watchlist")
selected_names = st.multiselect(
    "Bidding zones you're actively trading",
    ZONE_NAMES,
    default=current_names,
    help="Only these zones appear below — no noise from the full EU view.",
)
st.session_state["trader_watchlist"] = [BIDDING_ZONES[n] for n in selected_names]
watchlist = st.session_state["trader_watchlist"]

if not watchlist:
    st.info("Add at least one bidding zone to your watchlist to see forecasts.")
    st.stop()

# ---- Gather forecasts once for every watched zone ---------------------------
zone_data = {}
any_illustrative = False
for code in watchlist:
    df, is_live = fetch_forecast(code)
    any_illustrative = any_illustrative or not is_live
    zone_data[code] = {"df": df, "summary": forecast_summary(df)}

# ---- Triggered alerts (story 3) ---------------------------------------------
def _evaluate_alert(df, alert):
    """Return (triggered, first_date, first_value) for an alert against a
    forecast DataFrame, or (False, None, None)."""
    prices = df["predicted_price_eur_mwh"]
    if alert["direction"] == "above":
        hits = df[prices >= alert["threshold"]]
    else:
        hits = df[prices <= alert["threshold"]]
    if hits.empty:
        return False, None, None
    row = hits.iloc[0]
    return True, row["date"].date(), float(row["predicted_price_eur_mwh"])


triggered = []
for code in watchlist:
    alert = st.session_state["trader_alerts"].get(code)
    if not alert:
        continue
    fired, when, value = _evaluate_alert(zone_data[code]["df"], alert)
    if fired:
        triggered.append((code, alert, when, value))

if triggered:
    st.divider()
    st.write("##### 🔔 Alerts triggered")
    for code, alert, when, value in triggered:
        arrow = "above" if alert["direction"] == "above" else "below"
        st.warning(
            f"**{CODE_TO_NAME[code]}** — forecast crosses {arrow} your "
            f"€{alert['threshold']:.0f}/MWh threshold on **{when}** "
            f"(€{value:.1f}/MWh)."
        )

if any_illustrative:
    st.caption(
        "⚠️ Some forecasts are illustrative placeholders — the live ML1 "
        "endpoint is not returning data yet."
    )

# ---- Forecast comparison across the watchlist (story 2) ---------------------
st.divider()
st.write("##### 30-day forecast across your watchlist")

rows = []
for code in watchlist:
    s = zone_data[code]["summary"]
    rows.append({
        "Zone": CODE_TO_NAME[code],
        "Day 1 (€/MWh)": round(s["day1"], 1),
        "Day 30 (€/MWh)": round(s["day30"], 1),
        "30d trend": f"{s['trend_pct']:+.1f}%",
        "Avg (€/MWh)": round(s["avg"], 1),
        "Range (€/MWh)": f"{s['min']:.0f}–{s['max']:.0f}",
    })

table = pd.DataFrame(rows).set_index("Zone")
st.dataframe(table, use_container_width=True)
st.caption(
    "Every watched zone's price direction in one view — sort by trend to see "
    "where the model expects the biggest moves."
)

# ---- Per-zone detail + alert config -----------------------------------------
st.divider()
st.write("##### Zone detail")

tabs = st.tabs([CODE_TO_NAME[c] for c in watchlist])
for tab, code in zip(tabs, watchlist):
    with tab:
        s = zone_data[code]["summary"]
        df = zone_data[code]["df"]

        left, right = st.columns([3, 2])

        with left:
            fig = px.line(
                df, x="date", y="predicted_price_eur_mwh",
                labels={"date": "", "predicted_price_eur_mwh": "€/MWh"},
            )
            fig.add_hline(
                y=s["avg"], line_dash="dash", line_color="gray",
                annotation_text=f"avg €{s['avg']:.0f}",
            )
            alert = st.session_state["trader_alerts"].get(code)
            if alert:
                fig.add_hline(
                    y=alert["threshold"], line_dash="dot", line_color="orange",
                    annotation_text=f"alert €{alert['threshold']:.0f}",
                )
            zeus_plotly_layout(fig, height=320)
            st.plotly_chart(fig, use_container_width=True)

        with right:
            st.metric("30-day trend", f"{s['trend_pct']:+.1f}%",
                      f"€{s['day1']:.0f} → €{s['day30']:.0f}")
            st.metric("30-day average", f"€{s['avg']:.1f}/MWh")
            st.metric("Expected range", f"€{s['min']:.0f} – €{s['max']:.0f}")

            st.write("**Price alert**")
            alert = st.session_state["trader_alerts"].get(code)
            with st.form(f"alert_{code}"):
                direction = st.radio(
                    "Notify when forecast goes",
                    ["above", "below"],
                    index=0 if not alert or alert["direction"] == "above" else 1,
                    horizontal=True,
                )
                threshold = st.number_input(
                    "Threshold (€/MWh)", min_value=0.0, step=5.0,
                    value=float(alert["threshold"]) if alert else round(s["avg"], 0),
                )
                set_col, clear_col = st.columns(2)
                if set_col.form_submit_button("Set alert", use_container_width=True):
                    st.session_state["trader_alerts"][code] = {
                        "threshold": float(threshold), "direction": direction,
                    }
                    st.rerun()
                if clear_col.form_submit_button("Clear", use_container_width=True):
                    st.session_state["trader_alerts"].pop(code, None)
                    st.rerun()

st.divider()

nav_left, nav_right = st.columns(2)
with nav_left:
    if st.button("← Price Forecast", use_container_width=True):
        st.switch_page("pages/Price_Forecast.py")
with nav_right:
    if st.button("Trade Journal →", type="primary", use_container_width=True):
        st.switch_page("pages/Trade_Journal.py")
