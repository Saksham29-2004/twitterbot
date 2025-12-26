# app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings  # Assuming settings is where DATABASE_URL is defined

DATABASE_URL = settings.DATABASE_URL  # Make sure DATABASE_URL is set in your config

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # For SQLite
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
