# app/api/articles.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
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

@router.get("/articles")
def list_articles(db: Session = Depends(get_db)):
    data = (
        db.query(Article)
        .order_by(Article.created_at.desc())
        .limit(50)
        .all()
    )
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
