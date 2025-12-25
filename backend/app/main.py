from fastapi import FastAPI
from backend.app.scraper.ndtv import fetch
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from backend.app.db.database import engine, SessionLocal
from backend.app.db.models import Base, Article
from backend.app.scraper.ndtv import fetch
from datetime import datetime, date

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Disaster News Bot")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/scrape/ndtv")
def scrape_ndtv():
    return fetch()

@app.post("/ingest/ndtv")
def ingest_ndtv(db: Session = Depends(get_db)):
    articles = fetch()
    inserted = 0
    skipped = 0

    for a in articles:
        exists = db.query(Article).filter(Article.url == a["url"]).first()
        if exists:
            skipped += 1
            continue

        article = Article(
            source=a["source"],
            title=a["title"],
            url=a["url"],
            published=a.get("published", "")
        )

        db.add(article)
        inserted += 1

    db.commit()

    return {
        "fetched": len(articles),
        "inserted": inserted,
        "skipped_duplicates": skipped
    }

@app.get("/articles")
def list_articles(db: Session = Depends(get_db)):
    data = db.query(Article).order_by(Article.created_at.desc()).limit(50).all()

    return [
        {
            "id": a.id,
            "source": a.source,
            "title": a.title,
            "url": a.url,
            "published": a.published,
            "is_disaster": a.is_disaster,
            "tweeted": a.tweeted,
            "created_at": a.created_at
        }
        for a in data
    ]

@app.get("/dashboard/stats")
def dashboard_stats(db: Session = Depends(get_db)):
    total = db.query(Article).count()

    today = date.today()
    today_count = (
        db.query(Article)
        .filter(Article.created_at >= datetime.combine(today, datetime.min.time()))
        .count()
    )

    disasters = (
        db.query(Article)
        .filter(Article.is_disaster == True)
        .count()
    )

    tweeted = (
        db.query(Article)
        .filter(Article.tweeted == True)
        .count()
    )

    return {
        "total_articles": total,
        "articles_today": today_count,
        "disaster_articles": disasters,
        "tweeted_articles": tweeted
    }

@app.get("/dashboard/articles/disasters")
def disaster_articles(db: Session = Depends(get_db)):
    data = (
        db.query(Article)
        .filter(Article.is_disaster == True)
        .order_by(Article.created_at.desc())
        .limit(20)
        .all()
    )

    return [
        {
            "id": a.id,
            "title": a.title,
            "source": a.source,
            "published": a.published,
            "disaster_type": a.disaster_type,
            "tweeted": a.tweeted
        }
        for a in data
    ]

@app.get("/dashboard/health")
def dashboard_health(db: Session = Depends(get_db)):
    last = (
        db.query(Article)
        .order_by(Article.created_at.desc())
        .first()
    )

    return {
        "status": "ok",
        "last_article_ingested_at": last.created_at if last else None
    }
