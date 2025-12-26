# scraper/indiatoday.py

import feedparser

def fetch_indiatoday_rss(feed_url: str, source: str):
    feed = feedparser.parse(feed_url)
    items = []
    for entry in feed.entries:
        items.append({
            "source": source,
            "title": entry.get("title", ""),
            "url": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("description", ""),
            "is_disaster": False,  # Adjust based on your logic
            "disaster_type": None,
            "tweeted": False
        })
    return items
