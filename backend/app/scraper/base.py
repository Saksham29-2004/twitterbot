# scraper/base.py

from sqlalchemy.orm import Session
from app.db.models import Article

def ingest_articles(db: Session, feed_url: str, source: str, fetch_function):
    """
    A generic function to ingest articles from a specified RSS feed.
    
    Args:
        db (Session): Database session.
        feed_url (str): RSS feed URL.
        source (str): Source name (e.g., 'BBC', 'NDTV').
        fetch_function (function): Function to fetch and parse the RSS feed.
        
    Returns:
        dict: Number of articles inserted and skipped.
    """
    # Fetch articles from the RSS feed
    articles = fetch_function(feed_url, source)
    
    # Initialize counters for inserted and skipped articles
    inserted = 0
    skipped = 0

    # Loop over the fetched articles and insert them into the database
    for article_data in articles:
        # Check if the article already exists in the database to avoid duplicates
        exists = db.query(Article).filter(Article.url == article_data["url"]).first()
        
        # If article exists, skip it
        if exists:
            skipped += 1
            continue

        # Create a new Article object
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

        # Add the article to the session
        db.add(new_article)
        inserted += 1

    # Commit the session to save changes to the database
    db.commit()

    return {"inserted": inserted, "skipped": skipped}
