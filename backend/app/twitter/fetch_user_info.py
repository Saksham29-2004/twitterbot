from twitter_service import get_user_info

# Step 1: Use the access token
access_token = input("Enter your access token: ")

# Step 2: Fetch and display user info
user_info = get_user_info(access_token)
if user_info:
    print("User Info:", user_info)
