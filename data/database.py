import psycopg

def get_connection():
    raise NotImplementedError  # TODO: connect using your Postgres credentials


def clean_post(raw_post):
    # one raw post dict -> dict matching the posts table's columns:
    # post_id, created_utc, title, is_self, score, ups, upvote_ratio, author,
    # author_flair_text, location_lat, location_long, location_name, category,
    # link_flair_text, is_video, media, num_comments, num_crossposts,
    # num_reports, over_18, selftext, thumbnail, url, subreddit
    #
    # needed: 'id' -> 'post_id', 'created_utc' epoch -> datetime,
    # 'media' -> jsonb-compatible
    raise NotImplementedError


def clean_comments(raw_comments):
    # list of raw comment dicts (one post's worth) -> list of dicts matching
    # the comments table's columns: comment_id, post_id, created_utc,
    # parent_id, author, author_flair_text, body, score, permalink, ups, downs
    #
    # needed: 'id' -> 'comment_id', 'link_id' -> 'post_id' (strip 't3_'),
    # 'created_utc' epoch -> datetime, 'subreddit' has no column (drop it,
    # or add the column -- your call)
    raise NotImplementedError


def insert_post(conn, post):
    raise NotImplementedError  # TODO: INSERT the cleaned post into the posts table


def insert_comments(conn, comments):
    raise NotImplementedError  # TODO: INSERT the cleaned comments into the comments table
