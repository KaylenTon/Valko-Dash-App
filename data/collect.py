import requests
import time

# Collecting Valko-related Reddit posts and comments (via Arctic Redshift API) for analysis - storing into Postgres database

keywords = [
    "valko",
    "wolfie",
    "val",
    "sixth love interest",
    "6th love interest",
    "sixth li",
    "6th li",
    "new love interest",
    "new li",
    "werewolf",
    "werewolves"
]

post_fields = [
    'id',
    'created_utc',
    'title',
    'is_self',
    'score', # posts' net score (upvotes - downvotes)
    'ups', # total number of upvotes
    'upvote_ratio', # ratio of upvotes to total votes; ex: .89 means about 89% of votes are upvotes
    'author',
    'author_flair_text',
    'location_lat',
    'location_long',
    'location_name',
    'category',
    'link_flair_text',
    'is_video',
    'media',
    'num_comments',
    'num_crossposts',
    'num_reports',
    'over_18',
    'selftext',
    'thumbnail',
    'url',
    'subreddit',
    'retrieved_on'
]

posts_url = "https://arctic-shift.photon-reddit.com/api/posts/search"
comments_url = "https://arctic-shift.photon-reddit.com/api/comments/search"

headers = {
    "accept": "application/json"
}

posts_params = {
    'subreddit' : 'loveanddeepspace',
    'after' : '2026-06-22',
    'before' : '2026-07-12',
    'limit' : 100,
    'sort' : 'asc',
    'format' : 'json',
    'query' : 'valko'
}

comments_params = {
    'subreddit' : 'loveanddeepspace',
    'after' : '2026-06-22',
    'before' : '2026-07-12',
    'limit' : 100,
    'sort' : 'asc',
    'format' : 'json',
    'link_id' : 't3_valko'
}

post_response = requests.get(posts_url, headers=headers, params=posts_params)

print(post_response.status_code)
print(post_response.headers['content-type'])
# print(post_response.text)

post_data = post_response.json()
for post in post_data['data']:
    for field, value in post.items():
        print(f"{field}: {value}")
    print("\n---\n")

comment_response = requests.get(comments_url, headers=headers, params=comments_params)

# print(type(comment_response))
print(comment_response.status_code)
print(comment_response.headers['content-type'])
# print(comment_response.text)

print("\nStart of comment data\n")
comment_data = comment_response.json()
# print(f"\n{comment_data}\n")
for comment in comment_data['data']:
    for field, value in comment.items():
        print(f"{field}: {value}")
    print("\n---\n")

# ---------------
