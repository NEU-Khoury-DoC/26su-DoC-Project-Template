"""Global Zeus typography and theme overrides."""

import streamlit as st

_ZILLA_SLAB_FONT_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Zilla+Slab:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap"
)


def apply_zeus_theme() -> None:
    """Inject Zilla Slab across the Streamlit app for a bold, industrial look."""
    st.markdown(
        f"""
        <style>
            @import url('{_ZILLA_SLAB_FONT_URL}');

            html, body, [class*="css"] {{
                font-family: "Zilla Slab", serif !important;
            }}

            h1, h2, h3, h4, h5, h6,
            [data-testid="stMarkdownContainer"] h1,
            [data-testid="stMarkdownContainer"] h2,
            [data-testid="stMarkdownContainer"] h3 {{
                font-family: "Zilla Slab", serif !important;
                font-weight: 700 !important;
                letter-spacing: -0.01em;
            }}

            p, li, label, span, div, input, textarea, select {{
                font-family: "Zilla Slab", serif !important;
            }}

            [data-testid="stSidebar"] * {{
                font-family: "Zilla Slab", serif !important;
            }}

            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
                font-weight: 600 !important;
            }}

            .stButton button,
            .stPageLink a,
            [data-testid="stBaseButton-secondary"] {{
                font-family: "Zilla Slab", serif !important;
                font-weight: 600 !important;
            }}

            [data-testid="stMetricValue"] {{
                font-family: "Zilla Slab", serif !important;
                font-weight: 700 !important;
            }}

            [data-testid="stMetricLabel"] {{
                font-family: "Zilla Slab", serif !important;
                font-weight: 600 !important;
                text-transform: uppercase;
                letter-spacing: 0.04em;
                font-size: 0.8rem !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
