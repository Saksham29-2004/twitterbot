from pydantic_settings import BaseSettings  # Correct import for pydantic-settings
from typing import List, ClassVar
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings(BaseSettings):
    # Database settings (e.g., SQLite)
    DATABASE_URL: str = "sqlite:///./twitterbot.db"  # Default value for SQLite, replace as needed
    
    # List of allowed origins for CORS
    allow_origins: List[str] = ["http://localhost:5173"]  # List of allowed origins
    
    # Twitter API credentials (for posting tweets)
    TWITTER_API_KEY: str = os.getenv("TWITTER_API_KEY")  # Use environment variable
    TWITTER_API_SECRET_KEY: str = os.getenv("TWITTER_API_SECRET_KEY")  # Use environment variable
    TWITTER_ACCESS_TOKEN: str = os.getenv("TWITTER_ACCESS_TOKEN")  # Use environment variable
    TWITTER_ACCESS_TOKEN_SECRET: str = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")  # Use environment variable

    # Class-level constants (use ClassVar for non-Pydantic fields)
    CLIENT_ID: ClassVar[str] = os.getenv('CLIENT_ID', 'your_client_id_here')  # Use ClassVar for constants
    CLIENT_SECRET: ClassVar[str] = os.getenv('CLIENT_SECRET', 'your_client_secret_here')  # Use ClassVar for constants
    REDIRECT_URI: ClassVar[str] = os.getenv('REDIRECT_URI', 'https://9caae56956ea.ngrok-free.app')  # Example redirect URI
    
    # Optionally, if using a bearer token for v2 API, include that here
    TWITTER_BEARER_TOKEN: str = os.getenv("TWITTER_BEARER_TOKEN", None)  # Leave empty if you're not using v2 API
    
    class Config:
        # Load environment variables from a .env file
        env_file = ".env"  # This is where your sensitive credentials are loaded from
        extra = 'allow'  # Allow extra fields in the model

# Instantiate settings to access them in your app
settings = Settings()
