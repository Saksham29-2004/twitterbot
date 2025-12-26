from app.twitter.oauth_service import fetch_access_token

# Step 1: Input the authorization code
authorization_code = input("Enter the authorization code from the URL: ")

# Step 2: Fetch the access token
access_token = fetch_access_token(authorization_code)
print("Access token:", access_token)
