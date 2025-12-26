from app.config import settings  # Correct import for settings
from twitter_service import post_tweet
# Step 1: Use the access token to post a tweet
access_token = input("Enter your access token: ")
tweet_content = "Hello, this is my first tweet via OAuth 2.0!"

# Step 2: Post the tweet
tweet_response = post_tweet(tweet_content, access_token)

# Step 3: Print the tweet response
print(tweet_response)
