from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint
from datetime import datetime
from .database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String, index=True)
    title = Column(String)
    url = Column(String, nullable=False, unique=True)
    published = Column(String)

    is_disaster = Column(Boolean, default=False)
    disaster_type = Column(String, nullable=True)

    summary = Column(String, nullable=True)
    tweeted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("url", name="uq_article_url"),
    )
