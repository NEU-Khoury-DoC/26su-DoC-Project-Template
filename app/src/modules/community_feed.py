import streamlit as st
import requests

API_BASE = "http://web-api:4000"

def render_feed():
    user_id = st.session_state.get('user_id')
    role = st.session_state.get('role')

    options = ["All", "Farmers", "Policymakers", "Researchers"]
    map_to_state = {"All": "all", "Farmers": "farmer", "Policymakers": "politician", "Researchers": "researcher"}

    initial = "All"
    if 'feed_filter' in st.session_state:
        rev = {v:k for k,v in map_to_state.items()}
        initial = rev.get(st.session_state.get('feed_filter'), 'All')

    # style the radio to look like chip buttons
    st.markdown(
        """
        <style>
        /* scoped-ish chip-style for radio groups */
        div[role="radiogroup"] > div { display:inline-block; margin-right:8px; }
        div[role="radiogroup"] input[type="radio"]{ display:none; }
        div[role="radiogroup"] label {
            background:#f0f0f0;
            padding:10px 18px;
            border-radius:999px;
            cursor:pointer;
            color:#333;
            font-family: 'Courier New', monospace;
            border: 1px solid rgba(0,0,0,0.06);
        }
        div[role="radiogroup"] input[type="radio"]:checked + label {
            background: #6f49f6;
            color: #fff;
            border-color: #5b35e6;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    selected = st.radio('', options, index=options.index(initial), horizontal=True, key='feed_filter_radio')
    st.session_state['feed_filter'] = map_to_state[selected]

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