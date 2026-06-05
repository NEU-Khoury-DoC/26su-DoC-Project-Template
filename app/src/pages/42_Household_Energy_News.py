import logging

logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks()

st.title("EU Energy News")
st.write(
    "Latest headlines on electricity, gas, renewables, and related EU energy topics. "
    "Results use NewsData.io's top-domain filter for reputable sources and a broad "
    "energy keyword search across major EU countries. "
    "See [NewsData.io docs](https://newsdata.io/documentation#first-request)."
)

NEWS_API_URL = "http://web-api:4000/news/eu-energy"


def _format_countries(countries):
    if not countries:
        return "—"
    if isinstance(countries, list):
        return ", ".join(countries)
    return str(countries)


if st.button("Fetch EU energy news", type="primary", use_container_width=False):
    logger.info("Requesting EU energy news from %s", NEWS_API_URL)
    with st.spinner("Fetching latest EU energy articles..."):
        try:
            response = requests.get(NEWS_API_URL, timeout=20)
            response.raise_for_status()
            data = response.json()
            st.session_state["eu_energy_news"] = data
        except requests.exceptions.HTTPError:
            try:
                detail = response.json().get("error", response.text)
            except ValueError:
                detail = response.text
            st.error(f"Could not fetch news: {detail}")
        except requests.exceptions.RequestException as e:
            logger.error("EU energy news request failed: %s", e)
            st.error(f"Could not reach the API: {e}")
            st.info("Ensure the API container is running and NEWSDATA_API_KEY is set in api/.env.")

news = st.session_state.get("eu_energy_news")

if news:
    articles = news.get("articles", [])
    st.caption(
        f"Showing {len(articles)} of {news.get('totalResults', len(articles))} results "
        f"· EU countries: {news.get('countries', 'EU')} "
        f"· {news.get('sourceFilter', 'reputable sources')}"
    )

    if not articles:
        st.warning("No articles returned. Try again later.")
    else:
        for article in articles:
            title = article.get("title") or "Untitled"
            link = article.get("link")
            source = article.get("source_name") or "Unknown source"
            pub_date = article.get("pubDate") or "—"
            countries = _format_countries(article.get("country"))
            description = article.get("description") or ""

            with st.container(border=True):
                headline_col, meta_col = st.columns([3, 1])
                with headline_col:
                    if link:
                        st.markdown(f"**[{title}]({link})**")
                    else:
                        st.markdown(f"**{title}**")
                    if description:
                        st.write(description)
                with meta_col:
                    st.caption(f"**Source:** {source}")
                    st.caption(f"**Published:** {pub_date}")
                    st.caption(f"**Country:** {countries}")

                    image_url = article.get("image_url")
                    if image_url:
                        st.image(image_url, use_container_width=True)

else:
    st.info("Click **Fetch EU energy news** to load the latest articles.")

if st.button("Return to Dashboard"):
    st.switch_page("pages/40_Household_Owner_Dashboard.py")
