import os
import sqlite3
import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime

# ---------------- CONFIG ---------------- #

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw", "news")
DB_PATH = os.path.join(DATA_DIR, "metadata", "urls.db")

RSS_FEEDS = [
    "https://techcrunch.com/tag/startups/feed/",
    "https://yourstory.com/feed"
]

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# ---------------- DATABASE ---------------- #

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processed_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def url_exists(conn, url):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM processed_urls WHERE url=?", (url,))
    return cur.fetchone() is not None


def save_url(conn, url, source):
    cur = conn.cursor()
    cur.execute("INSERT INTO processed_urls (url, source) VALUES (?, ?)", (url, source))
    conn.commit()


# ---------------- TEXT CLEANING ---------------- #

def extract_clean_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove junk
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    article = soup.find("article") or soup

    paragraphs = [
        p.get_text(strip=True)
        for p in article.find_all("p")
        if len(p.get_text(strip=True)) > 50
    ]

    return "\n".join(paragraphs)


# ---------------- FETCH + PROCESS ---------------- #

def fetch_news():
    conn = sqlite3.connect(DB_PATH)

    for feed_url in RSS_FEEDS:
        print(f"\n🔍 Reading feed: {feed_url}")
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            url = entry.link

            if url_exists(conn, url):
                print("⏩ Skipped (already processed)")
                continue

            print("🆕 Fetching:", url)

            try:
                response = requests.get(url, timeout=10)
                text = extract_clean_text(response.text)
                text=text+" "+"source_url:"+url

                if len(text) < 300:
                    print("⚠️ Skipped (too short)")
                    continue

                filename = url.replace("https://", "").replace("/", "_") + ".txt"
                filepath = os.path.join(RAW_DIR, filename)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(text)

                save_url(conn, url, "funding_news")
                print("✅ Saved article")

            except Exception as e:
                print("❌ Error:", e)

    conn.close()


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    init_db()
    fetch_news()


