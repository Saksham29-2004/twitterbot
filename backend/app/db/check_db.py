# app/db/check_db.py
from app.db.database import SessionLocal
from app.db.models import Article

# Create a session
db = SessionLocal()

# Query all articles from the database
articles = db.query(Article).all()

# Print the results
if articles:
    for article in articles:
        print(f"Title: {article.title}, URL: {article.url}")
else:
    print("No articles found.")

# Close the session
db.close()
