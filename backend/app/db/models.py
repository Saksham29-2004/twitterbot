# app/db/models.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    title = Column(String)
    url = Column(String, unique=True)  # Ensure the URL is unique to prevent duplicates
    published = Column(DateTime)
    summary = Column(String)
    is_disaster = Column(Boolean, default=False)
    disaster_type = Column(String, nullable=True)
    tweeted = Column(Boolean, default=False)
