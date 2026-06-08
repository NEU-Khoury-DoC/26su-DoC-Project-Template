"""Global Zeus typography and theme overrides."""

import streamlit as st

_MONTSERRAT_FONT_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap"
)

# Streamlit renders chevrons and UI icons via Material Symbols; custom fonts must
# not override those glyphs or ligature names show as overlapping text.
_ICON_FONT_STACK = (
    '"Material Symbols Rounded", "Material Icons", "Material Icons Outlined", '
    '"Material Symbols Outlined", sans-serif'
)


def apply_zeus_theme() -> None:
    """Inject Montserrat across the Streamlit app."""
    st.markdown(
        f"""
        <style>
            @import url('{_MONTSERRAT_FONT_URL}');

            html, body, .stApp {{
                font-family: "Montserrat", sans-serif;
            }}

            h1, h2, h3, h4, h5, h6,
            [data-testid="stMarkdownContainer"] h1,
            [data-testid="stMarkdownContainer"] h2,
            [data-testid="stMarkdownContainer"] h3 {{
                font-family: "Montserrat", sans-serif !important;
                font-weight: 800 !important;
                letter-spacing: -0.02em;
            }}

            p, li, label, input, textarea, select, button, a {{
                font-family: "Montserrat", sans-serif;
            }}

            [data-testid="stSidebar"] {{
                font-family: "Montserrat", sans-serif;
            }}

            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
                font-weight: 600;
            }}

            [data-testid="stMetricValue"] {{
                font-family: "Montserrat", sans-serif !important;
                font-weight: 700 !important;
            }}

            [data-testid="stMetricLabel"] {{
                font-family: "Montserrat", sans-serif !important;
                font-weight: 600 !important;
                text-transform: uppercase;
                letter-spacing: 0.04em;
                font-size: 0.8rem !important;
            }}

            [data-testid="stIconMaterial"],
            [data-testid="stIconMaterial"] span,
            .material-icons,
            .material-symbols-rounded,
            .material-symbols-outlined {{
                font-family: {_ICON_FONT_STACK} !important;
                font-variation-settings: "FILL" 0, "wght" 400, "GRAD" 0, "opsz" 24 !important;
                letter-spacing: normal !important;
                text-transform: none !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
