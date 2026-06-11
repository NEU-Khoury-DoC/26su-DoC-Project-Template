"""Live ENTSO-E Transparency Platform data for the journalist pages.

ENTSO-E covers *electricity* only, so this module exposes the four indicators
that map cleanly onto it:

* Electricity Price   - day-ahead price (bidding zone)
* Electricity Demand  - actual total load (control area)
* Renewables Share    - actual generation by production type
* Import Dependence    - proxy: (demand - domestic generation) / demand

Every query goes to ENTSO-E live via ``entsoe-py`` and is wrapped in
``st.cache_data`` (1 hour TTL) so the pages stay responsive and we don't hammer
the API. Generation and load are fetched once per country and reused across the
derived indicators.

The API key is read from (in order): the ``ENTSOE_API_KEY`` env var (set via
``api/.env`` in Docker) or Streamlit secrets.
"""

import logging
import os

import pandas as pd
import streamlit as st

logger = logging.getLogger(__name__)

# Countries shown on the journalist pages. Cyprus and Malta are isolated
# island grids with no day-ahead market or published load/generation on
# ENTSO-E, so they're excluded to avoid all-N/A selections.
COUNTRIES = [
    "Austria", "Belgium", "Bulgaria", "Croatia",
    "Czech Republic", "Denmark", "Estonia", "Finland", "France",
    "Germany", "Greece", "Hungary", "Ireland", "Italy",
    "Latvia", "Lithuania", "Luxembourg", "Netherlands",
    "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
    "Spain", "Sweden",
]

# Day-ahead prices are published per *bidding zone*. For countries split into
# several zones we use the main/reference zone. Islands without a day-ahead
# market (Cyprus, Malta) have no entry and render as N/A.
PRICE_ZONE = {
    "Austria": "AT", "Belgium": "BE", "Bulgaria": "BG", "Croatia": "HR",
    "Czech Republic": "CZ", "Denmark": "DK_1", "Estonia": "EE", "Finland": "FI",
    "France": "FR", "Germany": "DE_LU", "Greece": "GR", "Hungary": "HU",
    "Ireland": "IE_SEM", "Italy": "IT_NORD", "Latvia": "LV", "Lithuania": "LT",
    "Luxembourg": "DE_LU", "Netherlands": "NL", "Poland": "PL", "Portugal": "PT",
    "Romania": "RO", "Slovakia": "SK", "Slovenia": "SI", "Spain": "ES",
    "Sweden": "SE_3",
}

# Load / generation are published per *control area* (whole country, even when
# the price market is split into zones).
COUNTRY_AREA = {
    "Austria": "AT", "Belgium": "BE", "Bulgaria": "BG", "Croatia": "HR",
    "Cyprus": "CY", "Czech Republic": "CZ", "Denmark": "DK", "Estonia": "EE",
    "Finland": "FI", "France": "FR", "Germany": "DE_LU", "Greece": "GR",
    "Hungary": "HU", "Ireland": "IE", "Italy": "IT", "Latvia": "LV",
    "Lithuania": "LT", "Luxembourg": "LU", "Malta": "MT", "Netherlands": "NL",
    "Poland": "PL", "Portugal": "PT", "Romania": "RO", "Slovakia": "SK",
    "Slovenia": "SI", "Spain": "ES", "Sweden": "SE",
}

# Group raw ENTSO-E production types into friendly buckets for the mix chart.
MIX_BUCKETS = {
    "Nuclear": ["Nuclear"],
    "Gas": ["Fossil Gas", "Fossil Coal-derived gas"],
    "Coal": ["Fossil Hard coal", "Fossil Brown coal/Lignite", "Fossil Peat",
             "Fossil Oil shale"],
    "Oil": ["Fossil Oil"],
    "Wind": ["Wind Onshore", "Wind Offshore"],
    "Solar": ["Solar"],
    "Hydro": ["Hydro Run-of-river and poundage", "Hydro Water Reservoir",
              "Hydro Pumped Storage"],
    "Biomass": ["Biomass"],
    "Other": ["Waste", "Geothermal", "Marine", "Other", "Other renewable"],
}

# Buckets counted as renewable for the Renewables Share indicator.
RENEWABLE_BUCKETS = {"Wind", "Solar", "Hydro", "Biomass"}

# Fixed order for the mix chart so it reads top-to-bottom consistently.
MIX_ORDER = list(MIX_BUCKETS.keys())


# ---- API key + client -------------------------------------------------------

def _api_key():
    """Resolve the ENTSO-E API key from env var or Streamlit secrets."""
    key = os.environ.get("ENTSOE_API_KEY")
    if key:
        return key.strip()
    try:
        if "ENTSOE_API_KEY" in st.secrets:
            return str(st.secrets["ENTSOE_API_KEY"]).strip()
    except Exception:
        pass
    return None


@st.cache_resource(show_spinner=False)
def _client():
    """One cached entsoe-py client per app session."""
    key = _api_key()
    if not key:
        return None
    from entsoe import EntsoePandasClient
    return EntsoePandasClient(api_key=key)


def has_api_key():
    return _api_key() is not None


def _window(days=3):
    """Recent time window in CET, the platform's reference timezone."""
    end = pd.Timestamp.now(tz="Europe/Brussels").floor("h")
    return end - pd.Timedelta(days=days), end


def _last_two(series):
    """Latest value and its change vs the previous point, tolerating gaps."""
    series = series.dropna()
    if series.empty:
        return None, None
    value = float(series.iloc[-1])
    delta = float(value - series.iloc[-2]) if len(series) >= 2 else None
    return value, delta


# ---- Raw fetchers (cached, one query each) ----------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def _price_daily(country):
    """Daily average day-ahead price (EUR/MWh) indexed by date, or None."""
    zone = PRICE_ZONE.get(country)
    client = _client()
    if not zone or client is None:
        return None
    try:
        start, end = _window()
        prices = client.query_day_ahead_prices(zone, start=start, end=end)
        return prices.resample("D").mean()
    except Exception as exc:  # NoMatchingDataError and transient API errors
        logger.warning("price query failed for %s (%s): %s", country, zone, exc)
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def _load_daily(country):
    """Daily mean actual load (MW) indexed by date, or None."""
    area = COUNTRY_AREA.get(country)
    client = _client()
    if not area or client is None:
        return None
    try:
        start, end = _window()
        load = client.query_load(area, start=start, end=end)
        return load.iloc[:, 0].resample("D").mean()
    except Exception as exc:
        logger.warning("load query failed for %s (%s): %s", country, area, exc)
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def _generation_daily(country):
    """Daily mean generation (MW) per friendly bucket, DataFrame or None."""
    area = COUNTRY_AREA.get(country)
    client = _client()
    if not area or client is None:
        return None
    try:
        start, end = _window()
        gen = client.query_generation(area, start=start, end=end)
        if isinstance(gen.columns, pd.MultiIndex):
            # Keep "Actual Aggregated"; drop the "Actual Consumption" columns
            # (e.g. pumped-storage pumping) so totals reflect generation.
            gen = gen.xs("Actual Aggregated", axis=1, level=1, drop_level=True)
        gen = gen.clip(lower=0)  # ignore negative consumption readings
        buckets = {}
        for bucket, types in MIX_BUCKETS.items():
            cols = [t for t in types if t in gen.columns]
            buckets[bucket] = gen[cols].sum(axis=1) if cols else 0.0
        daily = pd.DataFrame(buckets).resample("D").mean()
        return daily[daily.sum(axis=1) > 0]
    except Exception as exc:
        logger.warning("generation query failed for %s (%s): %s", country, area, exc)
        return None


# ---- Public indicators ------------------------------------------------------

def get_price(country):
    """(EUR/MWh, day-over-day change) for the latest day, or (None, None)."""
    daily = _price_daily(country)
    return _last_two(daily) if daily is not None else (None, None)


def get_demand(country):
    """(GWh/day, change) of electricity demand for the latest day."""
    daily = _load_daily(country)
    if daily is None:
        return None, None
    gwh = daily * 24 / 1000  # mean MW over a day -> GWh delivered that day
    return _last_two(gwh)


def get_renewables_share(country):
    """(% renewable generation, change in percentage points) for latest day."""
    daily = _generation_daily(country)
    if daily is None or daily.empty:
        return None, None
    total = daily.sum(axis=1)
    renew = daily[[b for b in RENEWABLE_BUCKETS if b in daily.columns]].sum(axis=1)
    share = (100 * renew / total).where(total > 0)
    return _last_two(share)


def get_import_dependence(country):
    """(% of demand met by net imports, change in pp) for latest day.

    Proxy = max(demand - domestic generation, 0) / demand. Negative net
    positions (net exporters) clamp to 0%.
    """
    load = _load_daily(country)
    gen = _generation_daily(country)
    if load is None or gen is None or gen.empty:
        return None, None
    gen_total = gen.sum(axis=1)
    df = pd.concat([load.rename("load"), gen_total.rename("gen")], axis=1).dropna()
    if df.empty:
        return None, None
    dep = (100 * (df["load"] - df["gen"]).clip(lower=0) / df["load"]).where(df["load"] > 0)
    return _last_two(dep)


def get_mix(country):
    """Generation mix for the latest day as a % Series indexed by bucket.

    Returns None when generation data is unavailable.
    """
    daily = _generation_daily(country)
    if daily is None or daily.empty:
        return None
    latest = daily.iloc[-1]
    total = latest.sum()
    if total <= 0:
        return None
    share = (100 * latest / total).reindex(MIX_ORDER).fillna(0.0)
    share.name = "Share (%)"
    return share


# Indicators surfaced on the comparison page: label -> (getter, unit, fmt).
COMPARISON_INDICATORS = {
    "Electricity Price (€/MWh)": (get_price, "€/MWh", "{:.1f}"),
    "Electricity Demand (GWh/day)": (get_demand, "GWh/day", "{:.0f}"),
    "Renewables Share (%)": (get_renewables_share, "%", "{:.1f}"),
    "Import Dependence (%)": (get_import_dependence, "%", "{:.1f}"),
}


def get_indicator_value(country, label):
    """Scalar value for a comparison indicator, or None."""
    getter = COMPARISON_INDICATORS[label][0]
    value, _delta = getter(country)
    return value
