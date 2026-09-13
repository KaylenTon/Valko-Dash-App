import requests
import time
import datetime
from datetime import datetime, timezone

headers = {
    "accept": "application/json"
}

posts_url = "https://arctic-shift.photon-reddit.com/api/posts/search"

comments_url = "https://arctic-shift.photon-reddit.com/api/comments/search"

RETRY_DELAY = 5
MAX_RETRIES = 8
REQUEST_DELAY = 1

keywords = "valko"

def paginate(url, params, until_epoch=None, label=""):
    params = dict(params)
    seen = set()
    results = []

    while True:

        # Keep retrying the request if the server says to slow down
        attempt = 0
        while True:
            response = requests.get(
                url,
                headers=headers,
                params=params
            )

            if response.status_code in (422, 429):
                attempt += 1
                if attempt > MAX_RETRIES:
                    raise RuntimeError(f"Gave up after {MAX_RETRIES} retries on {url}")
                wait = min(RETRY_DELAY * (2 ** (attempt - 1)), 60)
                print(f"Got {response.status_code}. Retrying in {wait} seconds...")
                time.sleep(wait)
                continue

            response.raise_for_status()

            page = response.json()['data']
            break

        if not page:
            break

        for item in page:
            if item['id'] not in seen:
                seen.add(item['id'])
                results.append(item)

        last_ts = page[-1]['created_utc']
        last_time = datetime.fromtimestamp(last_ts, tz=timezone.utc)

        print(f"[{label}] got {len(page)} (total so far: {len(results)}), up to {last_time}")

        if len(page) < params['limit'] or (
            until_epoch is not None and last_ts >= until_epoch
        ):
            break

        params['after'] = last_ts + 1

        time.sleep(REQUEST_DELAY)

    return results

def to_epoch(date_str):
    return int(
        datetime.strptime(date_str, '%Y-%m-%d')
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )

CHUNK_SECONDS = 5 * 24 * 3600  # 5 days — keeps each search call cheap enough to avoid timeouts

def daterange_chunks(after_epoch, before_epoch, chunk_seconds=CHUNK_SECONDS):
    start = after_epoch
    while start < before_epoch:
        end = min(start + chunk_seconds, before_epoch)
        yield start, end
        start = end

def get_matching_posts(keyword, subreddit, after_date, before_date):

    after_epoch = to_epoch(after_date)
    before_epoch = to_epoch(before_date)

    matched = {}

    for chunk_after, chunk_before in daterange_chunks(after_epoch, before_epoch):
        chunk_start = datetime.fromtimestamp(chunk_after, tz=timezone.utc)
        chunk_end = datetime.fromtimestamp(chunk_before, tz=timezone.utc)
        print(f"--- posts: searching {chunk_start} to {chunk_end} ---")

        params = {
            'subreddit': subreddit,
            'after': chunk_after,
            'before': chunk_before,
            'limit': 100,
            'sort': 'asc',
            'query': keyword
        }

        posts = paginate(
            posts_url,
            params,
            until_epoch=chunk_before,
            label="posts"
        )

        for post in posts:
            matched[post['id']] = post

        print(f"--- chunk done: {len(matched)} unique posts found so far ---")

        time.sleep(REQUEST_DELAY)

    return list(matched.values())

def get_comments_for_post(post_id):
    params = {
        'link_id': f't3_{post_id}',
        'limit': 100,
        'sort': 'asc'
    }

    return paginate(
        comments_url,
        params,
        until_epoch=None,
        label=f"comments/{post_id}"
    )

if __name__ == '__main__':
    posts = get_matching_posts(keywords, 'loveanddeepspace', '2026-06-22', '2026-06-23')
    print(f"Found {len(posts)} matching posts")

    all_comments = []
    for i, post in enumerate(posts, start=1):
        comments = get_comments_for_post(post['id'])
        all_comments.extend(comments)
        print(f"post {i}/{len(posts)} {post['id']}: {len(comments)} comments (total comments so far: {len(all_comments)})")
        time.sleep(REQUEST_DELAY)

    print(f"Total comments: {len(all_comments)}")
