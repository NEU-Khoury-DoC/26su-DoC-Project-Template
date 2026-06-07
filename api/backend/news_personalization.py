"""Map Zeus user profile fields to NewsData.io request parameters."""

from backend.ml_countries import ML_COUNTRY_OPTIONS

# NewsData.io language codes (ISO 639-1, lowercase).
LANGUAGE_TO_NEWS_CODE = {
    "Bulgarian": "bg",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "German": "de",
    "Greek": "el",
    "Hungarian": "hu",
    "Irish": "ga",
    "Italian": "it",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Maltese": "mt",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Spanish": "es",
    "Swedish": "sv",
}

ENERGY_CATEGORIES = "environment,business,science"

# Headline search terms in the user's language. qInTitle keeps results closer to energy topics.
ENERGY_TITLE_QUERY_BY_LANG = {
    "bg": "енергия OR електричество OR газ OR възобновяема",
    "cs": "energie OR elektřina OR plyn OR obnovitelné",
    "da": "energi OR el OR gas OR vedvarende",
    "de": "Energie OR Strom OR Energiewende OR Gas OR Erneuerbare",
    "el": "ενέργεια OR ηλεκτρικό OR αέριο OR ανανεώσιμη",
    "en": "energy OR electricity OR renewables OR grid OR gas OR utility",
    "es": "energía OR electricidad OR renovable OR gas OR solar",
    "et": "energia OR elekter OR gaas OR taastuv",
    "fi": "energia OR sähkö OR kaasu OR uusiutuva",
    "fr": "énergie OR électricité OR renouvelable OR gaz OR éolien",
    "ga": "energy OR fuinneamh OR leictreachas OR gás",
    "hr": "energija OR struja OR plin OR obnovljiva",
    "hu": "energia OR áram OR gáz OR megújuló",
    "it": "energia OR elettricità OR rinnovabile OR gas OR solare",
    "lt": "energija OR elektra OR dujos OR atsinaujinanti",
    "lv": "enerģija OR elektrība OR gāze OR atjaunojamā",
    "mt": "enerġija OR elettriku OR gass OR riġenerabbli",
    "nl": "energie OR elektriciteit OR hernieuwbaar OR gas OR wind",
    "pl": "energia OR prąd OR odnawialne OR gaz OR wiatr",
    "pt": "energia OR eletricidade OR renovável OR gás OR solar",
    "ro": "energie OR electricitate OR gaz OR regenerabilă",
    "sk": "energia OR elektrina OR plyn OR obnoviteľné",
    "sl": "energija OR elektrika OR plin OR obnovljiva",
    "sv": "energi OR el OR gas OR förnybar OR vind",
}

DEFAULT_ENERGY_TITLE_QUERY = (
    "energy OR electricity OR renewables OR gas OR grid OR utility"
)

# Same idea as above, but searches the full article body (q). Used as a fallback.
ENERGY_BODY_QUERY_BY_LANG = {
    "de": "Energie OR Strom OR Gas OR Erneuerbare OR Energiewende",
    "fr": "énergie OR électricité OR renouvelable OR gaz",
    "es": "energía OR electricidad OR renovable OR gas",
    "it": "energia OR elettricità OR rinnovabile OR gas",
    "nl": "energie OR elektriciteit OR hernieuwbaar OR gas",
    "pl": "energia OR prąd OR odnawialne OR gaz",
    "pt": "energia OR eletricidade OR renovável OR gás",
}

DEFAULT_ENERGY_BODY_QUERY = "energy OR electricity OR gas OR renewables OR climate"

# Used after NewsData responds to sort results and drop obvious off-topic matches.
ENERGY_RELEVANCE_KEYWORDS_BY_LANG = {
    "bg": ["енергия", "електричество", "газ", "възобнов"],
    "cs": ["energie", "elektřin", "plyn", "obnovitel"],
    "da": ["energi", "elpris", "gas", "vedvarende", "vind"],
    "de": [
        "energie", "strom", "gas", "erdgas", "netz", "kw", "mwh",
        "solar", "wind", "kraftwerk", "energiewende", "heiz", "tarif",
    ],
    "el": ["ενέργ", "ηλεκτρ", "αέρι", "ανανεώσι"],
    "en": [
        "energy", "electric", "electricity", "renewable", "gas", "grid",
        "solar", "wind", "kwh", "mwh", "utility", "tariff", "nuclear",
        "emissions", "power plant", "lng", "storage",
    ],
    "es": ["energía", "electricidad", "renovable", "gas", "solar", "eólica"],
    "et": ["energia", "elekter", "gaas", "taastuv"],
    "fi": ["energia", "sähkö", "kaasu", "uusiutuva", "tuuli"],
    "fr": ["énergie", "électricité", "renouvelable", "gaz", "éolien", "solaire"],
    "ga": ["energy", "fuinneamh", "leictreachas", "gás"],
    "hr": ["energij", "struj", "plin", "obnovljiv"],
    "hu": ["energia", "áram", "gáz", "megújuló"],
    "it": ["energia", "elettricità", "rinnovabile", "gas", "solare", "eolico"],
    "lt": ["energij", "elektr", "duj", "atsinaujin"],
    "lv": ["enerģij", "elektr", "gāz", "atjaunoj"],
    "mt": ["enerġij", "elettrik", "gass", "riġenerabbli"],
    "nl": ["energie", "elektriciteit", "hernieuwbaar", "gas", "wind", "zon"],
    "pl": ["energi", "prąd", "odnawial", "gaz", "wiatr", "solar"],
    "pt": ["energia", "eletricidade", "renovável", "gás", "solar", "eólica"],
    "ro": ["energie", "electric", "gaz", "regenerabil", "solar", "vânt"],
    "sk": ["energi", "elektrin", "plyn", "obnoviteľ"],
    "sl": ["energij", "elektrik", "plin", "obnovljiv"],
    "sv": ["energi", "el", "gas", "förnybar", "vind", "sol"],
}

SHARED_ENERGY_KEYWORDS = [
    "energy", "electric", "electricity", "renewable", "gas", "grid",
    "solar", "wind", "kwh", "mwh", "utility", "tariff", "emissions",
    "nuclear", "coal", "lng", "storage", "power plant",
]

NOISE_KEYWORDS = [
    "football", "soccer", "celebrity", "recipe", "fashion", "movie",
    "album", "concert", "bitcoin", "crypto", "nft", "horoscope",
    "dating", "wedding", "royal baby",
]


def resolve_news_country(country_name):
    # NewsData expects lowercase ISO country codes (e.g. de, fr).
    code = ML_COUNTRY_OPTIONS.get(country_name)
    if not code:
        return None, None
    return country_name, code.lower()


def resolve_news_language(language_name):
    if not language_name:
        return None, None
    code = LANGUAGE_TO_NEWS_CODE.get(language_name)
    if not code:
        return language_name, None
    return language_name, code


def resolve_user_news_filters(user_row):
    # Country and language come from the users table (Persona Info page).
    if not user_row:
        return None, "User not found"

    country_name, country_code = resolve_news_country(user_row.get("country"))
    if not country_code:
        return None, (
            "User country is not set or is not one of the supported EU countries. "
            "Update it on the Persona Info page."
        )

    language_name = user_row.get("language")
    _, language_code = resolve_news_language(language_name)
    if not language_code:
        return None, (
            "User language is not set or is not supported for news filtering. "
            "Update it on the Persona Info page."
        )

    return {
        "country_name": country_name,
        "country_code": country_code,
        "language_name": language_name,
        "language_code": language_code,
    }, None


def _energy_title_query(language_code):
    return ENERGY_TITLE_QUERY_BY_LANG.get(language_code, DEFAULT_ENERGY_TITLE_QUERY)


def _energy_body_query(language_code):
    return ENERGY_BODY_QUERY_BY_LANG.get(language_code, DEFAULT_ENERGY_BODY_QUERY)


def _base_params(api_key, filters):
    return {
        "apikey": api_key,
        "country": filters["country_code"],
        "language": filters["language_code"],
        "sort": "source",
        "datatype": "news",
    }


def build_news_request_strategies(filters, api_key):
    # Try tighter queries first, then widen until NewsData returns something.
    # Stacking every filter at once often comes back empty.
    language_code = filters["language_code"]
    title_query = _energy_title_query(language_code)
    body_query = _energy_body_query(language_code)
    base = _base_params(api_key, filters)

    return [
        # Most relevant: energy terms in the headline, limited to energy-related categories.
        {
            "label": "title + category",
            "query": title_query,
            "params": {**base, "qInTitle": title_query, "category": ENERGY_CATEGORIES},
        },
        # Widen to full-article search while keeping category filters.
        {
            "label": "body + category",
            "query": body_query,
            "params": {**base, "q": body_query, "category": ENERGY_CATEGORIES},
        },
        # Drop category if the combined filters still return nothing.
        {
            "label": "title only",
            "query": title_query,
            "params": {**base, "qInTitle": title_query},
        },
        {
            "label": "body only",
            "query": body_query,
            "params": {**base, "q": body_query},
        },
    ]


def build_news_request_params(filters, api_key):
    # Returns the first (strictest) strategy only.
    strategies = build_news_request_strategies(filters, api_key)
    strategy = strategies[0]
    return strategy["params"], strategy["query"]


def _article_text(article):
    parts = [article.get("title") or "", article.get("description") or ""]
    return " ".join(parts).lower()


def _keyword_hits(text, keywords):
    hits = 0
    for keyword in keywords:
        if keyword in text:
            hits += 1
    return hits


def score_article_relevance(article, language_code):
    # NewsData's own filters are loose, so we re-check title and description here.
    title = (article.get("title") or "").lower()
    description = (article.get("description") or "").lower()
    full_text = f"{title} {description}"

    lang_keywords = ENERGY_RELEVANCE_KEYWORDS_BY_LANG.get(language_code, [])
    keywords = list(dict.fromkeys([*lang_keywords, *SHARED_ENERGY_KEYWORDS]))

    title_hits = _keyword_hits(title, keywords)
    body_hits = _keyword_hits(description, keywords)

    if title_hits == 0 and body_hits == 0:
        return 0

    noise_in_title = _keyword_hits(title, NOISE_KEYWORDS)
    if noise_in_title and title_hits == 0:
        return 0  # e.g. sports/crypto headline with no energy terms

    score = (title_hits * 4) + (body_hits * 2)

    # Small nudge for articles tagged in the user's language; not a hard filter.
    article_language = (article.get("language") or "").lower()
    if article_language == language_code:
        score += 2
    elif article_language and article_language != language_code:
        score -= 1

    if noise_in_title:
        score -= 2

    return score


def rank_articles(articles, filters, min_score=1, max_results=25):
    language_code = filters["language_code"]
    scored = []
    for article in articles:
        score = score_article_relevance(article, language_code)
        scored.append((score, article))

    scored.sort(
        key=lambda item: (
            -item[0],
            item[1].get("source_priority") or 999_999,
        )
    )
    ranked = [article for score, article in scored if score >= min_score]
    if ranked:
        return ranked[:max_results]
    # If nothing clears min_score, still return the best available matches.
    return [article for _, article in scored[:max_results]]


def filter_and_rank_articles(articles, filters, min_score=3, max_results=25):
    # Start strict, then loosen so the UI does not go empty when the API is sparse.
    for threshold in (min_score, 2, 1):
        ranked = rank_articles(articles, filters, min_score=threshold, max_results=max_results)
        if ranked:
            return ranked
    return rank_articles(articles, filters, min_score=0, max_results=max_results)