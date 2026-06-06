import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import os

st.set_page_config(layout='wide')

SideBarLinks()

st.title("WIP FOR FARM BLOG")
st.write('yikyak but for farmers')

def resolve_api_base():
	candidates = []
	try:
		candidates.append(st.secrets["api_url"])
	except Exception:
		pass
	env_api = os.environ.get("API_URL") or os.environ.get("API_BASE")
	if env_api:
		candidates.append(env_api)
	candidates.append("http://api:4000")
	candidates.append("http://localhost:4000")

	for base in candidates:
		if not base:
			continue
		try:
			r = requests.get(f"{base}/posts/", timeout=1)
			if r.status_code < 500:
				return base.rstrip('/')
		except Exception:
			continue
	return "http://localhost:4000"


API_BASE = resolve_api_base()


def get_posts():
	try:
		r = requests.get(f"{API_BASE}/posts/")
		r.raise_for_status()
		return r.json()
	except Exception as e:
		st.error(f"Error fetching posts: {e}")
		return []


def get_post(post_id):
	try:
		r = requests.get(f"{API_BASE}/posts/{post_id}")
		r.raise_for_status()
		data = r.json()
		return data[0] if isinstance(data, list) and data else data
	except Exception as e:
		st.error(f"Error fetching post: {e}")
		return None


def create_post(payload):
	try:
		r = requests.post(f"{API_BASE}/posts/", json=payload)
		r.raise_for_status()
		st.success("Post created")
		return r.json()
	except Exception as e:
		st.error(f"Error creating post: {e}")
		return None


def update_post_api(post_id, payload):
	try:
		r = requests.put(f"{API_BASE}/posts/{post_id}", json=payload)
		r.raise_for_status()
		st.success("Post updated")
		return r.json()
	except Exception as e:
		st.error(f"Error updating post: {e}")
		return None


def delete_post_api(post_id):
	try:
		r = requests.delete(f"{API_BASE}/posts/{post_id}")
		r.raise_for_status()
		st.success("Post deleted")
		return True
	except Exception as e:
		st.error(f"Error deleting post: {e}")
		return False


st.header('Posts')
st.caption(f"API endpoint: {API_BASE}")

posts = get_posts()

# initialise editing set in session state
if 'editing_posts' not in st.session_state:
	st.session_state['editing_posts'] = set()

left, right = st.columns([2, 1])

with left:
	if not posts:
		st.info('No posts available')

	for p in posts:
		pid = p.get('post_id')
		title = p.get('title') or f"Post {pid}"

		with st.expander(title):
			# ── view mode ──────────────────────────────────────────────
			if pid not in st.session_state['editing_posts']:
				st.write(p.get('post_text'))
				if p.get('img'):
					st.write(f"Image: {p.get('img')}")
				st.caption(f"By {p.get('created_by')} (user_id={p.get('user_id')}) at {p.get('created_at')}")

				cols = st.columns([1, 1, 1])
				if cols[0].button('Edit', key=f"edit_{pid}"):
					st.session_state['editing_posts'].add(pid)
					st.rerun()
				if cols[1].button('Delete', key=f"del_{pid}"):
					if delete_post_api(pid):
						st.session_state['editing_posts'].discard(pid)
						st.rerun()
				if cols[2].button('View raw JSON', key=f"raw_{pid}"):
					st.json(p)

			# ── inline edit mode ────────────────────────────────────────
			else:
				st.info("✏️ Editing this post")
				with st.form(key=f"inline_edit_{pid}"):
					e_title = st.text_input('Title', value=p.get('title') or '')
					e_text = st.text_area('Text', value=p.get('post_text') or '')
					e_img = st.text_input('Image', value=p.get('img') or '')
					e_user = st.text_input('User ID', value=str(p.get('user_id') or ''))
					e_updated_by = st.text_input('Updated by', value=p.get('updated_by') or '')

					save_col, cancel_col = st.columns([1, 1])
					submitted = save_col.form_submit_button('💾 Save')
					cancelled = cancel_col.form_submit_button('✕ Cancel')

				if submitted:
					payload = {}
					if e_title != (p.get('title') or ''):
						payload['title'] = e_title
					if e_text != (p.get('post_text') or ''):
						payload['post_text'] = e_text
					if e_img != (p.get('img') or ''):
						payload['img'] = e_img
					if e_user != str(p.get('user_id') or ''):
						payload['user_id'] = int(e_user) if e_user else None
					if e_updated_by != (p.get('updated_by') or ''):
						payload['updated_by'] = e_updated_by
					if payload:
						update_post_api(pid, payload)
					else:
						st.info('No changes to update')
					st.session_state['editing_posts'].discard(pid)
					st.rerun()

				if cancelled:
					st.session_state['editing_posts'].discard(pid)
					st.rerun()

with right:
	st.subheader('Create new post')
	with st.form('create_post'):
		title = st.text_input('Title')
		post_text = st.text_area('Text')
		img = st.text_input('Image (url or id)', '')
		user_id = st.text_input('User ID')
		created_by = st.text_input('Created by', user_id)
		if st.form_submit_button('Create'):
			payload = {
				'title': title,
				'post_text': post_text,
				'img': img or None,
				'user_id': int(user_id) if user_id else None,
				'created_by': created_by or user_id,
			}
			create_post(payload)
			st.rerun()