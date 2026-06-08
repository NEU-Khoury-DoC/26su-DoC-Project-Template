import streamlit as st
import requests

API_BASE = "http://web-api:4000"

def render_feed():
    user_id = st.session_state.get('user_id')
    role = st.session_state.get('role')

    # filter chips
    # selected filter default
    if 'feed_filter' not in st.session_state:
        st.session_state['feed_filter'] = 'all'

    # custom CSS for selected/unselected buttons
    st.markdown("""
    <style>
    div.stButton > button[kind="primary"] {
        background-color: light grey;
        color: white;
        border: 1px solid light grey;
    }

    div.stButton > button[kind="secondary"] {
        background-color: white;
        color: black;
        border: 1px solid black;
    }
    </style>
    """, unsafe_allow_html=True)

    # filter chips
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button(
            "All",
            use_container_width=True,
            type="primary" if st.session_state['feed_filter'] == 'all' else "secondary"
        ):
            st.session_state['feed_filter'] = 'all'
            st.rerun()

    with col2:
        if st.button(
            "Farmers",
            use_container_width=True,
            type="primary" if st.session_state['feed_filter'] == 'farmer' else "secondary"
        ):
            st.session_state['feed_filter'] = 'farmer'
            st.rerun()

    with col3:
        if st.button(
            "Policymakers",
            use_container_width=True,
            type="primary" if st.session_state['feed_filter'] == 'politician' else "secondary"
        ):
            st.session_state['feed_filter'] = 'politician'
            st.rerun()

    with col4:
        if st.button(
            "Researchers",
            use_container_width=True,
            type="primary" if st.session_state['feed_filter'] == 'researcher' else "secondary"
        ):
            st.session_state['feed_filter'] = 'researcher'
            st.rerun()

    # fetch posts
    try:
        posts = requests.get(f"{API_BASE}/posts/").json()
    except:
        st.error("Could not load posts")
        return

    left, right = st.columns([2, 1])

    with right:
        st.subheader("Create a post")
        with st.form("create_post"):
            title = st.text_input("Title")
            text = st.text_area("What's on your mind?", height=100)
            if st.form_submit_button("Post", use_container_width=True):
                requests.post(f"{API_BASE}/posts/", json={
                    'title': title,
                    'post_text': text,
                    'user_id': user_id,
                    'created_by': str(user_id)
                })
                st.success("Posted!")
                st.rerun()

    with left:
        for post in posts:
            pid = post.get('post_id')
            post_user_id = post.get('user_id')

            # get the role of whoever made the post
            try:
                post_user = requests.get(f"{API_BASE}/users/id/{post_user_id}").json()
                post_role = post_user.get('user_type', 'farmer')
            except:
                post_role = 'farmer'

            # apply filter
            if st.session_state['feed_filter'] != 'all' and post_role != st.session_state['feed_filter']:
                continue

            # role badge
            badge = {'farmer': '🌾 Farmer', 'politician': '🏛 Policymaker', 'researcher': '🔬 Researcher'}.get(post_role, '')

            with st.expander(f"**{post.get('title')}** — {badge}"):
                st.write(post.get('post_text'))
                st.caption(f"Posted by {post.get('created_by')} · {post.get('created_at', '')}")

                # comments
                try:
                    comments = requests.get(f"{API_BASE}/posts/{pid}/comments").json()
                    if comments:
                        st.divider()
                        for c in comments:
                            st.markdown(f"> {c.get('texts')}")
                            st.caption(f"— user {c.get('user_id')}")
                except:
                    pass

                # reply form
                with st.form(f"reply_{pid}"):
                    reply_text = st.text_input("Reply")
                    if st.form_submit_button("Reply"):
                        requests.post(f"{API_BASE}/posts/{pid}/comments", json={
                            'texts': reply_text,
                            'user_id': user_id,
                            'created_by': str(user_id),
                            'post_id': pid
                        })
                        st.rerun()

                # delete — only your own posts
                if user_id == post_user_id:
                    if st.button("Delete", key=f"del_{pid}"):
                        requests.delete(f"{API_BASE}/posts/{pid}")
                        st.rerun()