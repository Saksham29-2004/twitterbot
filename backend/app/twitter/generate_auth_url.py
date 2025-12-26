from app.twitter.oauth_service import get_authorization_url

# Generate the URL
auth_url = get_authorization_url()

# Print the URL to visit
print("Go to the following URL to authorize the app:")
print(auth_url)
