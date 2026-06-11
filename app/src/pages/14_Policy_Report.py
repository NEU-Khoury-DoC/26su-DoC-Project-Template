import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from datetime import date
from fpdf import FPDF
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE = "http://web-api:4000"

st.title("Policy Report Builder")
st.write("Create and save a policy report based on your findings.")

COUNTRIES = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia',
             'Denmark', 'Estonia', 'Finland', 'Germany', 'Greece', 'Hungary',
             'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
             'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia',
             'Slovenia', 'Spain', 'Sweden']

CROPS = ['Barley', 'Durum wheat', 'Feed barley', 'Rye', 'Soft wheat']

def build_report_text(report_name, policymaker_name, report_date, countries_text, crops_text, findings, recommendations):
    return f"""POLICY REPORT
=============
Title: {report_name}
Author: {policymaker_name}
Date: {report_date}
Countries: {countries_text}
Crops: {crops_text}

FINDINGS
--------
{findings}

RECOMMENDATIONS
---------------
{recommendations}
"""

def generate_pdf(report_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in report_text.split('\n'):
        pdf.cell(200, 10, txt=line.encode('latin-1', 'replace').decode('latin-1'), ln=True)
    return bytes(pdf.output())

st.divider()

col1, col2 = st.columns(2)
with col1:
    report_name = st.text_input("Report title", placeholder="e.g. Soft Wheat Price Analysis 2025")
with col2:
    policymaker_name = st.text_input("Policymaker name", value=st.session_state.get('first_name', ''))

col3, col4 = st.columns(2)
with col3:
    report_date = st.date_input("Date", value=date.today())
with col4:
    st.write("")



countries = st.multiselect("Countries", COUNTRIES, placeholder="Select one or more countries")


crops = st.multiselect("Crops (optional)", CROPS, placeholder="Select crops if relevant")

st.divider()

findings = st.text_area("Findings", height=150,
    placeholder="Summarise the key data findings here...")

recommendations = st.text_area("Recommendations", height=150,
    placeholder="What actions or policies do you recommend?")

st.divider()

crops_text = ", ".join(crops) if crops else "All crops"
countries_text = ", ".join(countries) if countries else "None selected"

report_text = build_report_text(
    report_name, policymaker_name, report_date,
    countries_text, crops_text, findings, recommendations
)

col_save, col_pdf, col_txt, _ = st.columns([1, 1, 1, 2])

with col_save:
    if st.button("Save to database", type="primary", use_container_width=True):
        if not report_name:
            st.warning("Please enter a report title.")
        elif not countries:
            st.warning("Please select at least one country.")
        elif not findings:
            st.warning("Please enter your findings.")
        else:
            try:
                response = requests.post(f"{API_BASE}/reports/", json={
                    'title': report_name,
                    'texts': report_text,
                    'created_by': policymaker_name or str(st.session_state.get('user_id'))
                })
                if response.status_code == 201:
                    st.success("Report saved successfully!")
                else:
                    st.error(f"Could not save report: {response.json()}")
            except Exception as e:
                st.error(f"Error saving report: {e}")

with col_pdf:
    if report_name and findings:
        try:
            pdf_bytes = generate_pdf(report_text)
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"{report_name}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF error: {e}")
    else:
        st.button("Download PDF", disabled=True, use_container_width=True)

with col_txt:
    if report_name and findings:
        st.download_button(
            label="Download .txt",
            data=report_text,
            file_name=f"{report_name}.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.button("Download .txt", disabled=True, use_container_width=True)