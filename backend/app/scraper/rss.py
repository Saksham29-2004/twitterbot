import feedparser

def fetch_rss(feed_url: str, source: str):
    feed = feedparser.parse(feed_url)
    items = []

    for entry in feed.entries:
        items.append({
            "source": source,
            "title": entry.get("title", ""),
            "url": entry.get("link", ""),
            "published": entry.get("published", "")
        })

    return items
