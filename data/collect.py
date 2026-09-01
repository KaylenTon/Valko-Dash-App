import requests

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

base_url = "https://arctic-shift.photon-reddit.com/api/posts/search"

headers = {
    "accept": "application/json"
}

params = {
    'subreddit' : 'loveanddeepspace',
    'after' : '2026-06-22',
    'before' : '2026-07-12',
    'limit' : 3,
    'sort' : 'asc',
    'fields' : ['author', 'author_flair_text', 'created_utc', 'id', 'retrieved_on', 'subreddit', 'subreddit_id', 'link_flair_text', 'num_comments', 'title', 'url'],
    'format' : 'json',
    'query' : 'valko'
}

response = requests.get(base_url, headers=headers, params=params)
print(response.status_code)
print(response.text)