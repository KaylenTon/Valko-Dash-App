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

base_url = "https://arctic-shift.photon-reddit.com/search"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",  # Replace with your actual API key
    "Content-Type": "application/json"
}
params = {
    'subreddit' : 'loveanddeepspace',
    'after' : '2026-06-22',
    'before' : '2026-07-12',
    'limit' : 1,
    'sort' : 'asc',
    'fields' : '',
    'format' : 'json',
    'query' : 'valko'
}