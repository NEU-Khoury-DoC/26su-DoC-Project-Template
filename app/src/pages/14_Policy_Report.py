import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Community Reports & Alerts")
st.write("Policy makers can view, filter, and respond to community-reported agricultural and environmental issues.")

reports_data = pd.DataFrame({
    "ID": [1, 2, 3, 4, 5],
    "Date": ["2024-05-30", "2024-05-29", "2024-05-28", "2024-05-27", "2024-05-26"],
    "Type": ["Flooding", "Soil Erosion", "Crop Disease", "Water Shortage", "Road Damage"],
    "Location": ["East Farms", "River Valley", "South Plains", "West Hills", "North Valley"],
    "Severity": ["High", "Medium", "High", "Medium", "Low"],
    "Status": ["Under Review", "Open", "Open", "Under Review", "Resolved"],
    "Description": [
        "Severe flooding damaging wheat crops.",
        "Rapid soil erosion near riverbank.",
        "Unusual crop disease spotted in corn fields.",
        "Irrigation water not sufficient.",
        "Farm access road damaged by heavy rain."
    ],
    "lat": [50.860, 50.890, 50.850, 50.840, 50.879],
    "lon": [4.720, 4.740, 4.680, 4.660, 4.700]
})

col1, col2, col3, col4 = st.columns(4)

with col1:
    type_filter = st.selectbox("Filter by Type", ["All"] + list(reports_data["Type"].unique()))

with col2:
    severity_filter = st.selectbox("Severity", ["All", "High", "Medium", "Low"])

with col3:
    status_filter = st.selectbox("Status", ["All", "Open", "Under Review", "Resolved"])

with col4:
    date_filter = st.selectbox("Date Range", ["All", "Last 7 Days", "Last 30 Days"])

filtered_reports = reports_data.copy()

if type_filter != "All":
    filtered_reports = filtered_reports[filtered_reports["Type"] == type_filter]

if severity_filter != "All":
    filtered_reports = filtered_reports[filtered_reports["Severity"] == severity_filter]

if status_filter != "All":
    filtered_reports = filtered_reports[filtered_reports["Status"] == status_filter]

st.divider()

st.subheader("Reports List")

st.dataframe(
    filtered_reports[["ID", "Date", "Type", "Location", "Severity", "Status", "Description"]],
    use_container_width=True
)

st.divider()

map_col, summary_col = st.columns([1, 1])

with map_col:
    st.subheader("Reports on Map")

    if len(filtered_reports) > 0:
        st.map(filtered_reports, latitude="lat", longitude="lon", zoom=10)
    else:
        st.warning("No reports match your filters.")

with summary_col:
    st.subheader("Reports Summary")

    st.write(f"Total Reports: {len(filtered_reports)}")
    st.write(f"High Severity: {len(filtered_reports[filtered_reports['Severity'] == 'High'])}")
    st.write(f"Medium Severity: {len(filtered_reports[filtered_reports['Severity'] == 'Medium'])}")
    st.write(f"Low Severity: {len(filtered_reports[filtered_reports['Severity'] == 'Low'])}")
    st.write(f"Under Review: {len(filtered_reports[filtered_reports['Status'] == 'Under Review'])}")
    st.write(f"Resolved: {len(filtered_reports[filtered_reports['Status'] == 'Resolved'])}")

st.divider()

if st.button("Save Report View"):
    st.success("Report view saved!")
