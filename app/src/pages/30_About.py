from pathlib import Path

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks(show_home=True)

TEAM_MEMBERS = [
    {
        "name": "Anjali Patel",
        "image": "assets/team/headshot_1.jpg",
        "bio": "Hi! I'm Anjali, a second-year Finance and Data Science major at Northeastern. For Zeus, I built ML2 a winter gas storage stress classifier , and connected it to the journalist pages it powers in our app. My favorite parts of the Dialogue were exploring Strasbourg and the Digital Twins Workshop!",
        "linkedin_url": "https://www.linkedin.com/in/anjalipatel267/",
    },
    {
        "name": "Rayna Patel",
        "image": "assets/team/headshot_2.jpg",
        "bio": "Short bio coming soon.",
        "linkedin_url": "https://www.linkedin.com/in/rayna-m-patel/",
    },
    {
        "name": "Ari Spokony",
        "image": "assets/team/headshot_3.jpg",
        "bio": "Short bio coming soon.",
        "linkedin_url": "https://www.linkedin.com/in/ari-spokony-6a9907348/",
    },
    {
        "name": "Bobby Bress",
        "image": "assets/team/headshot_4.jpg",
        "bio": "Short bio coming soon.",
        "linkedin_url": "https://www.linkedin.com/in/bobbybress/",
    },
]


def show_headshot(image_path: str, member_name: str, width: int = 200) -> None:
    path = Path(image_path)
    if path.is_file():
        st.image(str(path), width=width)
    else:
        st.markdown(
            f"""
            <div style="
                border: 2px dashed #ccc;
                border-radius: 8px;
                padding: 3rem 1rem;
                text-align: center;
                color: #666;
                min-height: 200px;
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                Add headshot for {member_name}<br>
                <small><code>{image_path}</code></small>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.write("# About Zeus")

st.markdown(
    """
   Energy security is extremely important for countries across the world.
   Policymakers, journalists, and citizens need clear, country-level information to make critical decisions, but the data lives across fragmented sources like ENTSO-E, GIE, and Eurostat.
   Zeus will change that.
   
   The app pulls live data from official European energy sources into a single platform that turns raw signals into actionable insight for European Union countries. 
   It will help citizens understand their energy bills, give journalists the evidence to back stories on gas and electricity market stress, and equip policy analysts with the comparative country data needed to draft briefings quickly. 
   Zeus will forecast day-ahead electricity prices and flag unusual cross-border flow and storage behavior, surfacing the kinds of events that precede supply shocks rather than just reporting them afterward. It will also display each country's dependence on others for energy imports, current gas storage versus historical norms, a supply-shock risk score, and how each country compares to its neighbors, using machine learning to power its forecasts and vulnerability assessments.

    """
)

st.write("### Our Team")

for i, member in enumerate(TEAM_MEMBERS):
    show_headshot(member["image"], member["name"])
    st.markdown(f"**{member['name']}**")
    st.caption(member["bio"])
    st.link_button(
        "LinkedIn",
        member["linkedin_url"],
        type="secondary"    
        )
    if i < len(TEAM_MEMBERS) - 1:
        st.divider()

if st.button("Return to Home", type="secondary"):
    st.switch_page("Home.py")
