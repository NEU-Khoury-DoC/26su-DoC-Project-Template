"""EU countries supported by the electricity price forecast model (ML1)."""

ML_COUNTRY_OPTIONS = {
    "Austria": "AT",
    "Belgium": "BE",
    "Bulgaria": "BG",
    "Croatia": "HR",
    "Czech Republic": "CZ",
    "Spain": "ES",
    "France": "FR",
    "Germany": "DE",
    "Hungary": "HU",
    "Latvia": "LV",
    "Netherlands": "NL",
    "Poland": "PL",
    "Portugal": "PT",
    "Romania": "RO",
    "Slovakia": "SK",
}

ML_COUNTRY_NAMES = list(ML_COUNTRY_OPTIONS.keys())
COUNTRY_PLACEHOLDER = "Select a country"


def resolve_ml_country(country_name):
    if country_name and country_name in ML_COUNTRY_OPTIONS:
        return country_name
    return None


def ml_country_select_options(include_placeholder=True):
    if include_placeholder:
        return [COUNTRY_PLACEHOLDER, *ML_COUNTRY_NAMES]
    return ML_COUNTRY_NAMES


def ml_country_select_index(country_name, include_placeholder=True):
    options = ml_country_select_options(include_placeholder)
    if country_name in ML_COUNTRY_OPTIONS:
        return options.index(country_name)
    return 0
