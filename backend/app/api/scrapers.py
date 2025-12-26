# app/api/scrapers.py
from datetime import datetime
import logging
from fastapi import APIRouter, Depends,HTTPException 
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.scraper.rss import fetch_all_rss
from app.db.models import Article
from app.twitter.twitter_service import post_tweet
from pydantic import BaseModel


router = APIRouter()

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ingest news into the database from RSS
@router.post("/ingest/news")
def ingest_news(db: Session = Depends(get_db)):
    all_feeds = fetch_all_rss()  # This fetches the articles from RSS feeds
    inserted = 0
    skipped = 0

    logger.info(f"Fetched {len(all_feeds)} articles.")  # Log number of articles fetched

    for article_data in all_feeds:
        try:
            logger.info(f"Processing article: {article_data['title']} - {article_data['url']}")
            
            # Check if article already exists
            exists = db.query(Article).filter(Article.url == article_data["url"]).first()
            if exists:
                skipped += 1
                continue  # Skip if the article already exists in the database

            # Convert 'published' to a datetime object
            if article_data["published"]:
                try:
                    published_datetime = datetime.strptime(article_data["published"], "%a, %d %b %Y %H:%M:%S %z")
                except ValueError as e:
                    logger.error(f"Error parsing date for article {article_data['title']}: {e}")
                    published_datetime = None  # Set to None if parsing fails
            else:
                published_datetime = None  # If no published date is available

            # Insert the article if it doesn't already exist
            new_article = Article(
                source=article_data["source"],
                title=article_data["title"],
                url=article_data["url"],
                published=published_datetime,  # Store as datetime object
                summary=article_data.get("summary", ""),
                is_disaster=article_data["is_disaster"],
                disaster_type=article_data["disaster_type"],
                tweeted=article_data["tweeted"]
            )

            db.add(new_article)  # Add the new article to the session
            inserted += 1
            logger.info(f"Inserted article: {article_data['title']}")

        except Exception as e:
            logger.error(f"Error inserting article {article_data['title']}: {e}")
            continue  # Log the error but continue processing other articles

    db.commit()  # Commit the transaction to the database

    return {"inserted": inserted, "skipped": skipped}

# Route to get all articles from the database
@router.get("/articles")
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()  # Fetch all articles from the database
    return articles  # Returns all articles in JSON format

# Route to get an article by URL (or any other field)
@router.get("/article/{url}")
def get_article_by_url(url: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.url == url).first()  # Fetch by URL
    if article:
        return article
    return {"message": "Article not found"}

@router.get("/api/news")
def get_news(db: Session = Depends(get_db)):
    # Query all articles from the database
    articles = db.query(Article).all()  # Fetch all articles from the Article table
    
    if articles:
        return articles  # Return articles in JSON format
    return {"message": "No articles found in the database."}


class TweetRequest(BaseModel):
    content: str

@router.post("/tweet")
def tweet_article(payload: TweetRequest):
    return post_tweet(payload.content)

# @router.post("/scrapers/tweet")
# def tweet_article(tweet: TweetContent):
#     # Ensure that the content is not empty
#     if not tweet.content or len(tweet.content) == 0:
#         raise HTTPException(status_code=422, detail="Tweet content is required")

#     result = post_tweet(tweet.content)
#     return result