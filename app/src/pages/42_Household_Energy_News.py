import logging

logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.nav import SideBarLinks
from modules.zeus_api import get_eu_energy_news, get_user

st.set_page_config(layout="wide")

SideBarLinks()

st.title("EU Energy News")
st.write(
    "Headlines filtered to your profile country and language, with energy-focused "
    "title search, environment/business/science categories, and relevance scoring."
)

user_id = st.session_state.get("user_id")
if not user_id:
    st.error("No user is logged in. Return to Home and log in as a household owner.")
    st.stop()

try:
    account = get_user(user_id)
except requests.exceptions.RequestException as exc:
    st.error(f"Could not load your profile: {exc}")
    st.stop()

profile_country = account.get("country") or "not set"
profile_language = account.get("language") or "not set"
st.caption(
    f"Personalized for **{profile_country}** · **{profile_language}** "
    "(update on Persona Info to change filters)."
)


def _format_countries(countries):
    if not countries:
        return "—"
    if isinstance(countries, list):
        return ", ".join(countries)
    return str(countries)


if st.button("Fetch energy news for me", type="primary", use_container_width=False):
    logger.info("Requesting personalized EU energy news for user_id=%s", user_id)
    with st.spinner("Fetching latest energy articles for your profile..."):
        try:
            data = get_eu_energy_news(user_id)
            st.session_state["eu_energy_news"] = data
        except requests.exceptions.HTTPError as exc:
            try:
                detail = exc.response.json().get("error", exc.response.text)
            except (ValueError, AttributeError):
                detail = str(exc)
            st.error(f"Could not fetch news: {detail}")
            if "Persona Info" in str(detail):
                st.info("Set your country and language on the Persona Info page, then try again.")
        except requests.exceptions.RequestException as exc:
            logger.error("Personalized energy news request failed: %s", exc)
            st.error(f"Could not reach the API: {exc}")
            st.info("Ensure the API container is running and NEWSDATA_API_KEY is set in api/.env.")

news = st.session_state.get("eu_energy_news")

if news:
    articles = news.get("articles", [])
    st.caption(
        f"Showing {len(articles)} relevant articles "
        f"(from {news.get('rawTotalResults', len(articles))} API matches"
        f"{', strategy: ' + news['queryStrategy'] if news.get('queryStrategy') else ''}) "
        f"· Country: {news.get('country', profile_country)} "
        f"· Language: {news.get('language', profile_language)}"
    )

    if not articles:
        st.warning("No articles returned for your profile. Try again later or adjust Persona Info.")
    else:
        for article in articles:
            title = article.get("title") or "Untitled"
            link = article.get("link")
            source = article.get("source_name") or "Unknown source"
            pub_date = article.get("pubDate") or "—"
            countries = _format_countries(article.get("country"))
            article_language = article.get("language") or "—"
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
                    st.caption(f"**Language:** {article_language}")

                    image_url = article.get("image_url")
                    if image_url:
                        st.image(image_url, use_container_width=True)

else:
    st.info("Click **Fetch energy news for me** to load articles for your country and language.")

if st.button("Return to Dashboard"):
    st.switch_page("pages/40_Household_Owner_Dashboard.py")
