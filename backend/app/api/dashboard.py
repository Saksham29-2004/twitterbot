# app/api/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.db.models import Article
from app.db.database import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard/stats")
def dashboard_stats(db: Session = Depends(get_db)):
    today = date.today()

    return {
        "total_articles": db.query(Article).count(),
        "articles_today": db.query(Article)
            .filter(Article.created_at >= datetime.combine(today, datetime.min.time()))
            .count(),
        "disaster_articles": db.query(Article)
            .filter(Article.is_disaster == True)
            .count(),
        "tweeted_articles": db.query(Article)
            .filter(Article.tweeted == True)
            .count()
    }

@router.get("/dashboard/articles/disasters")
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
