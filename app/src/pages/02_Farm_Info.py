import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://web-api:4000"

user_id = st.session_state['user_id']

if st.session_state.get("_farms_owner") != user_id:
    st.session_state.pop("farms", None)
    st.session_state["_farms_owner"] = user_id

# ── helpers ──────────────────────────────────────────────────────────────────

def load_farms(user_id):
    try:
        r = requests.get(f"{API_BASE}/farms/user/{int(user_id)}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data if isinstance(data, list) else [data]
        elif r.status_code == 404:
            return []
        else:
            st.error(f"Could not load farms (HTTP {r.status_code}).")
            return []
    except (requests.RequestException, ValueError):
        st.error("Could not reach the server. Please try again.")
        return []


def load_growing_data(farm_id):
    try:
        r = requests.get(f"{API_BASE}/user_growing/farm/{farm_id}", timeout=10)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 404:
            return []
        else:
            return []
    except (requests.RequestException, ValueError):
        return []


# ── dialogs ──────────────────────────────────────────────────────────────────

@st.dialog("Add a new farm")
def dialog_add_farm(user_id):
    st.write("Fill in the details for your new farm and its first location.")
    farm_name = st.text_input("Farm name")
    st.markdown("**First location**")
    country   = st.text_input("Country")
    lat       = st.number_input("Latitude",  value=0.0, format="%.6f")
    lon       = st.number_input("Longitude", value=0.0, format="%.6f")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create farm", type="primary", use_container_width=True):
            if not farm_name.strip():
                st.warning("Farm name is required.")
                return
            payload = {
                "farm_name":  farm_name.strip(),
                "user_id":    user_id,
                "created_by": str(user_id),
                "country":    country.strip(),
                "latitude":   lat,
                "longitude":  lon,
            }
            r = requests.post(f"{API_BASE}/farms/", json=payload, timeout=10)
            if r.status_code == 201:
                st.success("Farm created!")
                st.session_state["farms_dirty"] = True
                st.rerun()
            else:
                st.error(f"Failed to create farm: {r.text}")
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


@st.dialog("Edit farm name")
def dialog_edit_farm(farm):
    new_name = st.text_input("Farm name", value=farm.get("farm_name", ""))
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save", type="primary", use_container_width=True):
            if not new_name.strip():
                st.warning("Farm name cannot be empty.")
                return
            payload = {"farm_name": new_name.strip(), "updated_by": str(farm["user_id"])}
            r = requests.put(f"{API_BASE}/farms/farm_id/{farm['farm_id']}", json=payload, timeout=10)
            if r.status_code == 200:
                st.success("Farm name updated.")
                st.session_state["farms_dirty"] = True
                st.rerun()
            else:
                st.error(f"Update failed: {r.text}")
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


@st.dialog("Delete farm")
def dialog_delete_farm(farm):
    st.warning(
        f"Are you sure you want to delete **{farm.get('farm_name', 'this farm')}**? "
        "This will also remove all its locations and growing records."
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, delete", type="primary", use_container_width=True):
            r = requests.delete(f"{API_BASE}/farms/farm_id/{farm['farm_id']}", timeout=10)
            if r.status_code == 200:
                st.success("Farm deleted.")
                st.session_state["farms_dirty"] = True
                st.rerun()
            else:
                st.error(f"Delete failed: {r.text}")
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


@st.dialog("Add location")
def dialog_add_location(farm):
    st.write(f"Adding a new location for **{farm.get('farm_name')}**.")
    country = st.text_input("Country")
    lat     = st.number_input("Latitude",  value=0.0, format="%.6f")
    lon     = st.number_input("Longitude", value=0.0, format="%.6f")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add location", type="primary", use_container_width=True):
            payload = {
                "farm_id":    farm["farm_id"],
                "country":    country.strip(),
                "latitude":   lat,
                "longitude":  lon,
                "created_by": str(farm["user_id"]),
            }
            r = requests.post(f"{API_BASE}/farm_loc/", json=payload, timeout=10)
            if r.status_code == 201:
                st.success("Location added.")
                st.session_state["farms_dirty"] = True
                st.rerun()
            else:
                st.error(f"Failed to add location: {r.text}")
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


@st.dialog("Delete location")
def dialog_delete_location(farm_id, location_id):
    st.warning("Remove this location from the farm?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, remove", type="primary", use_container_width=True):
            r = requests.delete(f"{API_BASE}/farm_loc/location/{location_id}", timeout=10)
            if r.status_code == 200:
                st.success("Location removed.")
                st.session_state["farms_dirty"] = True
                st.rerun()
            else:
                st.error(f"Failed: {r.text}")
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


@st.dialog("Log growing record")
def dialog_add_growing(farm):
    st.write(f"Logging a new growing record for **{farm.get('farm_name')}**.")
    col1, col2 = st.columns(2)
    with col1:
        crop         = st.text_input("Crop type")
        season       = st.selectbox("Season", ["Kharif", "Rabi", "Zaid", "Summer", "Winter", "Whole Year"])
        sown         = st.date_input("Date sown")
        harvested    = st.date_input("Date harvested")
        water_source = st.selectbox("Water source", ["rainfed", "irrigated", "mixed"])
    with col2:
        n    = st.number_input("Nitrogen (N)",  min_value=0.0, format="%.2f")
        p    = st.number_input("Phosphorus (P)", min_value=0.0, format="%.2f")
        k    = st.number_input("Potassium (K)", min_value=0.0, format="%.2f")
        temp = st.number_input("Temperature (°C)", format="%.1f")
        rh   = st.number_input("Relative humidity (%)", min_value=0.0, max_value=100.0, format="%.1f")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save record", type="primary", use_container_width=True):
            if not crop.strip():
                st.warning("Crop type is required.")
                return
            payload = {
                "farm_id":           farm["farm_id"],
                "n":                 n,
                "p":                 p,
                "k":                 k,
                "type_of_crop":      crop.strip(),
                "season":            season,
                "sown":              str(sown),
                "harvested":         str(harvested),
                "water_source":      water_source,
                "temp":              temp,
                "relative_humidity": rh,
                "created_by":        str(farm["user_id"]),
            }
            r = requests.post(f"{API_BASE}/user_growing/", json=payload, timeout=10)
            if r.status_code == 201:
                st.success("Growing record saved.")
                st.session_state["farms_dirty"] = True
                st.rerun()
            else:
                st.error(f"Failed to save record: {r.text}")
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


@st.dialog("Edit growing record")
def dialog_edit_growing(record, record_id, user_id):
    st.write("Update the values for this growing record.")
    col1, col2 = st.columns(2)
    with col1:
        crop         = st.text_input("Crop type",         value=record.get("type_of_crop", ""))
        season       = st.selectbox("Season", ["Kharif", "Rabi", "Zaid", "Summer", "Winter", "Whole Year"],
                                    index=["Kharif", "Rabi", "Zaid", "Summer", "Winter", "Whole Year"].index(record.get("season", "Kharif")) if record.get("season") in ["Kharif", "Rabi", "Zaid", "Summer", "Winter", "Whole Year"] else 0)
        water_source = st.selectbox("Water source", ["rainfed", "irrigated", "mixed"],
                                    index=["rainfed", "irrigated", "mixed"].index(record.get("water_source", "rainfed")) if record.get("water_source") in ["rainfed", "irrigated", "mixed"] else 0)
    with col2:
        n    = st.number_input("Nitrogen (N)",       value=float(record.get("n", 0)),    format="%.2f")
        p    = st.number_input("Phosphorus (P)",      value=float(record.get("p", 0)),    format="%.2f")
        k    = st.number_input("Potassium (K)",       value=float(record.get("k", 0)),    format="%.2f")
        temp = st.number_input("Temperature (°C)",    value=float(record.get("temp", 0)), format="%.1f")
        rh   = st.number_input("Relative humidity (%)", value=float(record.get("relative_humidity", 0)),
                                min_value=0.0, max_value=100.0, format="%.1f")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save changes", type="primary", use_container_width=True):
            payload = {
                "n": n, "p": p, "k": k,
                "type_of_crop":      crop.strip(),
                "season":            season,
                "water_source":      water_source,
                "temp":              temp,
                "relative_humidity": rh,
                "updated_by":        str(user_id),
            }
            r = requests.put(f"{API_BASE}/user_growing/{record_id}", json=payload, timeout=10)
            if r.status_code == 200:
                st.success("Record updated.")
                st.session_state["farms_dirty"] = True
                st.rerun()
            else:
                st.error(f"Update failed: {r.text}")
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


@st.dialog("Delete growing record")
def dialog_delete_growing(record_id):
    st.warning("Permanently delete this growing record?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, delete", type="primary", use_container_width=True):
            r = requests.delete(f"{API_BASE}/user_growing/{record_id}", timeout=10)
            if r.status_code == 200:
                st.success("Record deleted.")
                st.session_state["farms_dirty"] = True
                st.rerun()
            else:
                st.error(f"Delete failed: {r.text}")
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


# ── page ─────────────────────────────────────────────────────────────────────

# reload farms when data changes
if st.session_state.get("farms_dirty") or "farms" not in st.session_state:
    if user_id is not None:
        st.session_state["farms"] = load_farms(user_id)
    else:
        st.session_state["farms"] = []
    st.session_state["farms_dirty"] = False

farms = st.session_state.get("farms", [])

# ── header row ───────────────────────────────────────────────────────────────
st.title("Farm Management")
st.write("Manage your farms, locations, and growing records.")

header_col1, header_col2 = st.columns([6, 1])
with header_col2:
    if user_id and st.button("＋ Add farm", type="primary", use_container_width=True):
        dialog_add_farm(user_id)

st.subheader("Your farms")

if not farms:
    st.info("You haven't registered any farms yet. Use the '+ Add farm' button above to get started!")
else:
    for farm in farms:
        farm_id   = farm.get("farm_id")
        farm_name = farm.get("farm_name", "Unnamed Farm")

        with st.expander(f"**{farm_name}**"):

            # ── farm meta + action buttons ────────────────────────────────
            meta_col, btn_col = st.columns([4, 2])
            with meta_col:
                st.write(f"**Owner:** {farm.get('owner_name', 'N/A')}")
                st.write(f"**Farm ID:** {farm_id}")
                st.write(f"**Created:** {farm.get('created_at', 'N/A')}")
            with btn_col:
                if st.button("✏️ Rename farm", key=f"edit_farm_{farm_id}", use_container_width=True):
                    dialog_edit_farm(farm)
                if st.button("🗑️ Delete farm", key=f"del_farm_{farm_id}", use_container_width=True):
                    dialog_delete_farm(farm)

            st.divider()

            # ── locations ─────────────────────────────────────────────────
            loc_hdr, loc_btn = st.columns([4, 2])
            with loc_hdr:
                st.markdown("**Locations**")
            with loc_btn:
                if st.button("＋ Add location", key=f"add_loc_{farm_id}", use_container_width=True):
                    dialog_add_location(farm)

            locations = farm.get("locations", [])
            if locations:
                for loc in locations:
                    loc_col, del_col = st.columns([5, 1])
                    with loc_col:
                        st.write(
                            f"{loc.get('country', 'Unknown')} — "
                            f"lat {loc.get('latitude')}, lng {loc.get('longitude')}"
                        )
                    with del_col:
                        if st.button("✕", key=f"del_loc_{loc.get('location_id')}", use_container_width=True):
                            dialog_delete_location(farm_id, loc.get("location_id"))
            else:
                st.caption("_No locations registered for this farm._")

            st.divider()

            # ── growing records ───────────────────────────────────────────
            grow_hdr, grow_btn = st.columns([4, 2])
            with grow_hdr:
                st.markdown("**Growing records**")
            with grow_btn:
                if st.button("＋ Log record", key=f"add_grow_{farm_id}", use_container_width=True):
                    dialog_add_growing(farm)

            records = load_growing_data(farm_id)
            if records:
                for idx, rec in enumerate(records):
                    rid = rec.get("user_growing_data_id")
                    if not rid:
                        st.error("Record is missing an ID, cannot edit or delete.")
                        continue
                    with st.container(border=True):
                        r_col1, r_col2, r_col3 = st.columns([3, 3, 1])
                        with r_col1:
                            st.write(f" **{rec.get('type_of_crop')}** — {rec.get('season')}")
                            st.caption(f"Sown: {rec.get('sown')}  →  Harvested: {rec.get('harvested')}  ({rec.get('duration_days', '?')} days)")
                        with r_col2:
                            st.write(f"{rec.get('water_source').capitalize()}  | {rec.get('temp')}°C  | {rec.get('relative_humidity')}% RH")
                            st.caption(f"N: {rec.get('n')}  P: {rec.get('p')}  K: {rec.get('k')}")
                        with r_col3:
                            if st.button("✏️", key=f"edit_rec_{rid}", use_container_width=True, help="Edit"):
                                dialog_edit_growing(rec, rid, user_id)
                            if st.button("🗑️", key=f"del_rec_{rid}", use_container_width=True, help="Delete"):
                                dialog_delete_growing(rid)
            else:
                st.caption("_No growing records logged for this farm yet._")