import os
import math
from pathlib import Path
from dotenv import load_dotenv
import psycopg
from psycopg.types.json import Jsonb
import pandas as pd

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

POST_COLUMNS = [
    'post_id', 'created_utc', 'title', 'is_self', 'score', 'ups',
    'upvote_ratio', 'author', 'author_flair_text', 'location_lat',
    'location_long', 'location_name', 'category', 'link_flair_text',
    'is_video', 'media', 'num_comments', 'num_crossposts',
    'num_reports', 'over_18', 'selftext', 'thumbnail', 'url', 'subreddit'
]

COMMENT_COLUMNS = [
    'comment_id', 'post_id', 'created_utc', 'parent_id', 'author',
    'author_flair_text', 'body', 'score', 'permalink', 'ups', 'downs', 'subreddit'
]

def get_connection():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ.get("DB_PASSWORD", ""),
    )


def clean_post(raw_post):
    df = pd.DataFrame([raw_post])

    df = df.rename(columns={'id': 'post_id'})
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s', utc=True)

    # reindex (not df[POST_COLUMNS]) so a post missing a field (e.g. no
    # 'category') gets NaN for that column instead of raising KeyError
    df = df.reindex(columns=POST_COLUMNS)

    # media is still a raw nested dict/None here -- insert_post will need
    # to handle turning it into something jsonb-compatible

    return df.iloc[0].to_dict()


def clean_comments(raw_comments):
    if not raw_comments:
        return []

    df = pd.DataFrame(raw_comments)

    df = df.rename(columns={'id': 'comment_id', 'link_id': 'post_id'})
    df['post_id'] = df['post_id'].str.removeprefix('t3_')
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s', utc=True)

    df = df.reindex(columns=COMMENT_COLUMNS)

    return df.to_dict('records')


def _none_if_nan(value):
    # .reindex() fills missing fields with float NaN, not None -- psycopg
    # doesn't know how to adapt NaN into most column types, so swap it out
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


def insert_post(conn, post):
    post = {k: _none_if_nan(v) for k, v in post.items()}
    if post['media'] is not None:
        post['media'] = Jsonb(post['media'])

    column_list = ", ".join(POST_COLUMNS)
    placeholders = ", ".join(f"%({col})s" for col in POST_COLUMNS)

    sql = f"""
        INSERT INTO posts ({column_list})
        VALUES ({placeholders})
        ON CONFLICT (post_id) DO NOTHING
    """

    with conn.cursor() as cur:
        cur.execute(sql, post)
    conn.commit()


def insert_comments(conn, comments):
    if not comments:
        return

    comments = [{k: _none_if_nan(v) for k, v in c.items()} for c in comments]

    column_list = ", ".join(COMMENT_COLUMNS)
    placeholders = ", ".join(f"%({col})s" for col in COMMENT_COLUMNS)

    sql = f"""
        INSERT INTO comments ({column_list})
        VALUES ({placeholders})
        ON CONFLICT (comment_id) DO NOTHING
    """

    with conn.cursor() as cur:
        cur.executemany(sql, comments)
    conn.commit()
