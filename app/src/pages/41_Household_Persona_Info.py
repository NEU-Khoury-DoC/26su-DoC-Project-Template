import datetime
import logging

logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.nav import SideBarLinks
from modules.zeus_api import (
    create_household_profile,
    delete_household_profile,
    get_household_profile,
    update_household_profile,
)

st.set_page_config(layout="wide")

SideBarLinks()

st.title("Household Persona Info")
st.write(
    "Save your household details so Zeus can personalize price forecasts, "
    "bill reminders, and country-level energy context."
)

user_id = st.session_state.get("user_id")
if not user_id:
    st.error("No user is logged in. Return to Home and log in as a household owner.")
    st.stop()

COUNTRIES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus",
    "Czech Republic", "Denmark", "Estonia", "Finland", "France",
    "Germany", "Greece", "Hungary", "Ireland", "Italy",
    "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
    "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
    "Spain", "Sweden",
]

BILLING_FREQUENCIES = ["Weekly", "Monthly", "Quarterly", "Annually"]
TARIFF_TYPES = ["Fixed rate", "Variable rate", "Time-of-use"]


def _empty_profile():
    return {
        "household_name": "",
        "email": "",
        "country": "Germany",
        "utility_provider": "",
        "monthly_bill_amount": 0.0,
        "bill_due_date": datetime.date.today(),
        "billing_frequency": "Monthly",
        "avg_monthly_kwh": 0.0,
        "tariff_type": "Variable rate",
        "notes": "",
    }


def _profile_from_api(row):
    profile = _empty_profile()
    if not row:
        return profile, False

    profile.update({
        "household_name": row.get("household_name", ""),
        "email": row.get("email", ""),
        "country": row.get("country", "Germany"),
        "utility_provider": row.get("utility_provider", ""),
        "monthly_bill_amount": float(row.get("monthly_bill_amount") or 0),
        "billing_frequency": row.get("billing_frequency", "Monthly"),
        "avg_monthly_kwh": float(row.get("avg_monthly_kwh") or 0),
        "tariff_type": row.get("tariff_type", "Variable rate"),
        "notes": row.get("notes") or "",
    })
    due = row.get("bill_due_date")
    if isinstance(due, str):
        profile["bill_due_date"] = datetime.date.fromisoformat(due)
    elif isinstance(due, datetime.date):
        profile["bill_due_date"] = due
    return profile, True


def _payload_from_form(profile):
    due = profile["bill_due_date"]
    return {
        "household_name": profile["household_name"],
        "email": profile["email"],
        "country": profile["country"],
        "utility_provider": profile["utility_provider"],
        "monthly_bill_amount": profile["monthly_bill_amount"],
        "bill_due_date": due.isoformat() if hasattr(due, "isoformat") else due,
        "billing_frequency": profile["billing_frequency"],
        "avg_monthly_kwh": profile["avg_monthly_kwh"],
        "tariff_type": profile["tariff_type"],
        "notes": profile["notes"] or "",
    }


try:
    saved_row = get_household_profile(user_id)
except requests.exceptions.RequestException as exc:
    st.error(f"Could not load profile from the API: {exc}")
    st.stop()

profile, has_profile = _profile_from_api(saved_row)

if has_profile:
    st.success(
        f"Profile saved for **{profile['household_name'] or 'your household'}** "
        f"in **{profile['country']}**."
    )
else:
    st.info("No household profile saved yet. Fill in the form below to create one.")

st.divider()

with st.form("household_profile_form"):
    st.subheader("Household details")

    name_col, email_col = st.columns(2)
    with name_col:
        household_name = st.text_input(
            "Household / contact name *",
            value=profile["household_name"],
            help="Used to label your saved profile.",
        )
    with email_col:
        email = st.text_input(
            "Email *",
            value=profile["email"],
            help="Contact email for alerts and account recovery.",
        )

    country_col, provider_col = st.columns(2)
    with country_col:
        country_index = (
            COUNTRIES.index(profile["country"])
            if profile["country"] in COUNTRIES
            else 0
        )
        country = st.selectbox("Country *", COUNTRIES, index=country_index)
    with provider_col:
        utility_provider = st.text_input(
            "Utility provider *",
            value=profile["utility_provider"],
            help="Your electricity supplier (e.g. E.ON, Enel, Iberdrola).",
        )

    st.subheader("Billing details")

    bill_col, due_col, freq_col = st.columns(3)
    with bill_col:
        monthly_bill_amount = st.number_input(
            "Typical bill amount (€) *",
            min_value=0.0,
            step=1.0,
            value=float(profile["monthly_bill_amount"]),
            help="Average amount you pay per billing cycle, in euros.",
        )
    with due_col:
        bill_due_date = st.date_input(
            "Next bill due date *",
            value=profile["bill_due_date"],
        )
    with freq_col:
        billing_frequency = st.selectbox(
            "Billing frequency *",
            BILLING_FREQUENCIES,
            index=BILLING_FREQUENCIES.index(profile["billing_frequency"]),
        )

    usage_col, tariff_col = st.columns(2)
    with usage_col:
        avg_monthly_kwh = st.number_input(
            "Average monthly usage (kWh) *",
            min_value=0.0,
            step=10.0,
            value=float(profile["avg_monthly_kwh"]),
            help="Typical electricity consumption; used for price and usage forecasts.",
        )
    with tariff_col:
        tariff_type = st.selectbox(
            "Tariff type *",
            TARIFF_TYPES,
            index=TARIFF_TYPES.index(profile["tariff_type"]),
        )

    notes = st.text_area(
        "Notes (optional)",
        value=profile["notes"],
        help="Anything else relevant to your household energy setup.",
    )

    submitted = st.form_submit_button(
        "Save profile" if has_profile else "Create profile",
        type="primary",
        use_container_width=True,
    )

    if submitted:
        required = {
            "Household / contact name": household_name.strip(),
            "Email": email.strip(),
            "Country": country,
            "Utility provider": utility_provider.strip(),
            "Typical bill amount": monthly_bill_amount > 0,
            "Average monthly usage": avg_monthly_kwh > 0,
        }
        missing = [label for label, ok in required.items() if not ok]

        if missing:
            st.error(f"Please complete all required fields: {', '.join(missing)}.")
        elif "@" not in email:
            st.error("Please enter a valid email address.")
        else:
            updated_profile = {
                "household_name": household_name.strip(),
                "email": email.strip(),
                "country": country,
                "utility_provider": utility_provider.strip(),
                "monthly_bill_amount": monthly_bill_amount,
                "bill_due_date": bill_due_date,
                "billing_frequency": billing_frequency,
                "avg_monthly_kwh": avg_monthly_kwh,
                "tariff_type": tariff_type,
                "notes": notes.strip(),
            }
            payload = _payload_from_form(updated_profile)
            try:
                if has_profile:
                    update_household_profile(user_id, payload)
                else:
                    create_household_profile(user_id, payload)
            except requests.exceptions.HTTPError as exc:
                st.error(f"Could not save profile: {exc}")
            except requests.exceptions.RequestException as exc:
                st.error(f"Could not reach the API: {exc}")
            else:
                logger.info("Household profile saved for user_id=%s", user_id)
                st.success("Household profile saved.")
                st.rerun()

st.divider()

if has_profile:
    st.subheader("Saved profile")
    view_col1, view_col2 = st.columns(2)
    with view_col1:
        st.markdown(f"**Name:** {profile['household_name']}")
        st.markdown(f"**Email:** {profile['email']}")
        st.markdown(f"**Country:** {profile['country']}")
        st.markdown(f"**Utility provider:** {profile['utility_provider']}")
        st.markdown(f"**Tariff type:** {profile['tariff_type']}")
    with view_col2:
        st.markdown(f"**Bill amount:** €{profile['monthly_bill_amount']:,.2f}")
        st.markdown(f"**Next due date:** {profile['bill_due_date']}")
        st.markdown(f"**Billing frequency:** {profile['billing_frequency']}")
        st.markdown(f"**Avg. usage:** {profile['avg_monthly_kwh']:,.0f} kWh/month")
        if profile["notes"]:
            st.markdown(f"**Notes:** {profile['notes']}")

    if st.button("Delete saved profile", type="secondary"):
        try:
            delete_household_profile(user_id)
        except requests.exceptions.RequestException as exc:
            st.error(f"Could not delete profile: {exc}")
        else:
            logger.info("Household profile deleted for user_id=%s", user_id)
            st.warning("Household profile deleted.")
            st.rerun()

if st.button("Return to Dashboard"):
    st.switch_page("pages/40_Household_Owner_Dashboard.py")
