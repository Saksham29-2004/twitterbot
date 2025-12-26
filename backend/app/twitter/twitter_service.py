import requests
from app.config import settings  # Correct import for settings

# Function to get user info with the access token
def get_user_info(access_token):
    url = "https://api.x.com/2/users/me"  # Endpoint to get authenticated user info
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return user_data
    else:
        print("Error fetching user info:", response.text)
        return None

# Function to post a tweet using the access token
def post_tweet(content, access_token):
    tweet_url = "https://api.x.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": content
    }
    response = requests.post(tweet_url, headers=headers, json=payload)

    if response.status_code == 201:
        tweet_data = response.json()
        print("Tweet successfully posted:", tweet_data['id'])
        return tweet_data
    else:
        print("Error posting tweet:", response.text)
        return None
