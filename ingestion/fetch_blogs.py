import os
import requests
import feedparser
import sqlite3
from bs4 import BeautifulSoup
import re

# ---------------- CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw", "blogs")
DB_PATH = os.path.join(DATA_DIR, "metadata", "urls2.db")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

BLOG_FEEDS = [
    "https://visible.vc/blog/top-vcs-in-india-startup-funding-guide/"
]

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS processed_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            source TEXT,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def url_exists(conn, url):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM processed_urls WHERE url=?", (url,))
    return cur.fetchone() is not None


def save_url(conn, url, title):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO processed_urls (url, source, title) VALUES (?, ?, ?)",
        (url, "blog", title)
    )
    conn.commit()


# ---------------- CONTENT EXTRACTION ----------------
def extract_text(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text() for p in paragraphs)

        if len(text.split()) < 150:
            return None
        return text.strip()

    except:
        return None


# ---------------- MAIN PIPELINE ----------------
def fetch_blogs():
    conn = sqlite3.connect(DB_PATH)

    for feed_url in BLOG_FEEDS:
        print(f"\n🔍 Reading feed: {feed_url}")
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            url = entry.link
            title = entry.title

            if url_exists(conn, url):
                print("⏩ Skipped:", title)
                continue

            print("📰 Fetching:", title)
            text = extract_text(url)

            if not text:
                print("⚠️ Skipped (no content)")
                continue

            filename = re.sub(r"[^\w\-]", "_", title)[:150] + ".txt"
            filepath = os.path.join(RAW_DIR, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)

            save_url(conn, url, title)
            print("✅ Saved")

    conn.close()


# ---------------- RUN ----------------
if __name__ == "__main__":
    init_db()
    fetch_blogs()
