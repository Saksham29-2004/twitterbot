# scraper/rss.py

from sqlalchemy.orm import Session
from app.db.database import SessionLocal  # Assuming SessionLocal is defined here
from app.db.models import Article  # Import Article model here
from app.scraper.toi import fetch_toi_rss
from app.scraper.ndtv import fetch_ndtv_rss
from app.scraper.thehindu import fetch_thehindu_rss
from app.scraper.indiatoday import fetch_indiatoday_rss
from app.scraper.economictimes import fetch_economictimes_rss
from app.scraper.base import ingest_articles

def fetch_rss(feed_url: str, source: str):
    """
    Call the appropriate RSS fetch function based on the source.
    """
    if source == "toi":
        return fetch_toi_rss(feed_url, source)
    elif source == "ndtv":
        return fetch_ndtv_rss(feed_url, source)
    elif source == "thehindu":
        return fetch_thehindu_rss(feed_url, source)
    elif source == "indiatoday":
        return fetch_indiatoday_rss(feed_url, source)
    elif source == "economictimes":
        return fetch_economictimes_rss(feed_url, source)
    else:
        raise ValueError(f"Unknown source: {source}")

def ingest_articles_from_sources(db: Session):
    # List of RSS feed URLs from multiple Indian news sources
    feeds = [
        ("https://timesofindia.indiatimes.com/rssfeedstopstories.cms", "toi"),
        ("https://feeds.ndtv.com/rss/topstories", "ndtv"),
        ("https://www.thehindu.com/news/national/?service=rss", "thehindu"),
        ("https://www.indiatoday.in/rss/1206519", "indiatoday"),
        ("https://economictimes.indiatimes.com/rssfeedstopstories.cms", "economictimes"),
    ]

    inserted = 0
    skipped = 0

    for feed_url, source in feeds:
        articles = fetch_rss(feed_url, source)

        for article_data in articles:
            exists = db.query(Article).filter(Article.url == article_data["url"]).first()
            if exists:
                skipped += 1
                continue

            new_article = Article(
                source=article_data["source"],
                title=article_data["title"],
                url=article_data["url"],
                published=article_data["published"],
                summary=article_data.get("summary", ""),
                is_disaster=article_data["is_disaster"],
                disaster_type=article_data["disaster_type"],
                tweeted=article_data["tweeted"]
            )
            db.add(new_article)
            inserted += 1

    db.commit()  # Save changes to the database
    return {"inserted": inserted, "skipped": skipped}

def fetch_all_rss():
    # Define the RSS feed URLs for each source
    urls = {
        "toi": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "ndtv": "https://feeds.ndtv.com/rss/topstories",
        "thehindu": "https://www.thehindu.com/news/national/?service=rss",
        "indiatoday": "https://www.indiatoday.in/rss/1206519",
        "economictimes": "https://economictimes.indiatimes.com/rssfeedstopstories.cms"
    }

    all_feeds = []

    # Call each of the fetch functions for the various sources, passing the URL and source
    all_feeds.extend(fetch_toi_rss(urls["toi"], "toi"))
    all_feeds.extend(fetch_ndtv_rss(urls["ndtv"], "ndtv"))
    all_feeds.extend(fetch_thehindu_rss(urls["thehindu"], "thehindu"))
    all_feeds.extend(fetch_indiatoday_rss(urls["indiatoday"], "indiatoday"))
    all_feeds.extend(fetch_economictimes_rss(urls["economictimes"], "economictimes"))
    
    return all_feeds