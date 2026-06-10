"""
Seed mock posts, comments, and reactions by POSTing to the running API.
Usage:
  API_BASE=http://localhost:4000 python3 scripts/seed_mock_api.py
If API_BASE not set, defaults to http://localhost:4000
"""

import os
import sys
import time
import requests

API_BASE = os.environ.get('API_BASE', 'http://localhost:4000')

posts_payload = [
    {
        'title': 'Planting schedule tips for spring',
        'post_text': "Any tips for adjusting planting schedules with unpredictable rainfall?",
        'user_id': 1,
        'created_by': 'mock_seed'
    },
    {
        'title': 'Best compost mixtures?',
        'post_text': "I've been mixing compost with wood chips; any recommendations?",
        'user_id': 2,
        'created_by': 'mock_seed'
    },
    {
        'title': 'Proposed subsidy for smallholders',
        'post_text': 'We propose targeted subsidies for water-efficient irrigation systems. Thoughts?',
        'user_id': 51,
        'created_by': 'mock_seed'
    },
    {
        'title': 'Market regulation impact study',
        'post_text': 'How will price caps affect small farmers in rural areas?',
        'user_id': 58,
        'created_by': 'mock_seed'
    },
    {
        'title': 'Soil moisture sensors dataset available',
        'post_text': 'I collected soil moisture data across 10 farms; sharing methodology and results.',
        'user_id': 52,
        'created_by': 'mock_seed'
    },
    {
        'title': 'New crop yield model draft',
        'post_text': "I'm testing a simple ML model for predicting yields based on NPK and rainfall.",
        'user_id': 62,
        'created_by': 'mock_seed'
    }
]

# comments keyed by index in posts_payload
comments_payload = {
    0: [
        {'texts': "I've had good results starting seedlings indoors 2 weeks earlier.", 'user_id': 3, 'created_by': 'mock_seed'},
        {'texts': 'Try adding more nitrogen in early growth stages.', 'user_id': 4, 'created_by': 'mock_seed'},
    ],
    1: [
        {'texts': 'Have you considered vermicompost? Works well.', 'user_id': 5, 'created_by': 'mock_seed'},
    ],
    2: [
        {'texts': 'We support the subsidy; it would help modernize irrigation.', 'user_id': 59, 'created_by': 'mock_seed'},
        {'texts': 'There may be unintended consequences; needs pilot testing.', 'user_id': 52, 'created_by': 'mock_seed'},
    ],
    3: [
        {'texts': 'Price caps could discourage supply; maybe targeted vouchers instead.', 'user_id': 51, 'created_by': 'mock_seed'},
    ],
    4: [
        {'texts': 'I can share the dataset and preprocessing steps.', 'user_id': 70, 'created_by': 'mock_seed'},
    ],
    5: [
        {'texts': 'Can you publish the model code? Would like to reproduce.', 'user_id': 74, 'created_by': 'mock_seed'},
    ]
}

# reactions: for each post index, list of reactions with pos_neg and user_id
reactions_payload = {
    0: [
        {'pos_neg': True, 'user_id': 10, 'created_by': 'mock_seed'},
        {'pos_neg': True, 'user_id': 2, 'created_by': 'mock_seed'},
        {'pos_neg': False, 'user_id': 15, 'created_by': 'mock_seed'},
    ],
    2: [
        {'pos_neg': True, 'user_id': 58, 'created_by': 'mock_seed'},
        {'pos_neg': True, 'user_id': 62, 'created_by': 'mock_seed'},
    ],
    3: [
        {'pos_neg': False, 'user_id': 16, 'created_by': 'mock_seed'},
    ],
    4: [
        {'pos_neg': True, 'user_id': 52, 'created_by': 'mock_seed'},
    ],
    5: [
        {'pos_neg': True, 'user_id': 74, 'created_by': 'mock_seed'},
        {'pos_neg': False, 'user_id': 23, 'created_by': 'mock_seed'},
    ]
}


def post_post(session, payload):
    url = f"{API_BASE}/posts/"
    r = session.post(url, json=payload, timeout=5)
    return r


def post_comment(session, post_id, payload):
    url = f"{API_BASE}/posts/{post_id}/comments"
    r = session.post(url, json=payload, timeout=5)
    return r


def post_reaction(session, post_id, payload):
    url = f"{API_BASE}/reactions/post/{post_id}"
    r = session.post(url, json=payload, timeout=5)
    return r


def main():
    print(f"Seeding mock data to {API_BASE}")
    sess = requests.Session()

    created_posts = []

    # create posts
    for i, p in enumerate(posts_payload):
        try:
            r = post_post(sess, p)
        except Exception as e:
            print(f"Failed to POST post idx={i}: {e}")
            sys.exit(1)

        if r.status_code not in (200,201):
            print(f"Failed to create post idx={i}: {r.status_code} {r.text}")
            sys.exit(1)

        data = r.json()
        new_id = data.get('post_id') or data.get('postId')
        print(f"Created post idx={i} -> id={new_id}")
        created_posts.append(new_id)
        time.sleep(0.1)

    # create comments
    for idx, comments in comments_payload.items():
        post_idx = idx
        if post_idx >= len(created_posts):
            print(f"Skipping comments for post idx={post_idx} (no created post)")
            continue
        post_id = created_posts[post_idx]
        for c in comments:
            try:
                r = post_comment(sess, post_id, c)
            except Exception as e:
                print(f"Failed to POST comment for post {post_id}: {e}")
                continue
            if r.status_code not in (200,201):
                print(f"Failed to create comment on post {post_id}: {r.status_code} {r.text}")
            else:
                print(f"Created comment on post {post_id}")
            time.sleep(0.05)

    # create reactions
    for idx, reacts in reactions_payload.items():
        if idx >= len(created_posts):
            print(f"Skipping reactions for post idx={idx} (no created post)")
            continue
        post_id = created_posts[idx]
        for rx in reacts:
            try:
                r = post_reaction(sess, post_id, rx)
            except Exception as e:
                print(f"Failed to POST reaction for post {post_id}: {e}")
                continue
            if r.status_code not in (200,201):
                print(f"Failed to create reaction on post {post_id}: {r.status_code} {r.text}")
            else:
                print(f"Created reaction on post {post_id}")
            time.sleep(0.05)

    print('Seeding complete')


if __name__ == '__main__':
    main()
