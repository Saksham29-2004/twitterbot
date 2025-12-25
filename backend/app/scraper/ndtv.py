from .rss import fetch_rss

NDTV_RSS = "https://feeds.feedburner.com/ndtvnews-india-news"

def fetch():
    data = fetch_rss(NDTV_RSS, "NDTV")
    print("DEBUG RSS COUNT:", len(data))
    return data
