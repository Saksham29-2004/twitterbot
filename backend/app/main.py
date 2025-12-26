# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.articles import router as articles_router
from app.api.dashboard import router as dashboard_router
from app.api.scrapers import router as scrapers_router
from app.db.database import engine, SessionLocal
from app.db.models import Base
from app.config import settings
from app.twitter.routes import router as twitter_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Disaster News Bot")

# CORS for React dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers for different modules
app.include_router(articles_router, prefix="/articles", tags=["articles"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
app.include_router(scrapers_router, prefix="/scrapers", tags=["scrapers"])
app.include_router(twitter_router)

@app.get("/")
def root():
    return {"status": "Backend running"}
