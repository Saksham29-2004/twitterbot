import base64
import hashlib
import os
import secrets
import urllib.parse
import requests
from app.config import settings

AUTH_URL = "https://twitter.com/i/oauth2/authorize"
TOKEN_URL = "https://api.twitter.com/2/oauth2/token"

# In-memory (OK for dev)
_pkce_store = {}

def _base64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def get_authorization_url():
    code_verifier = _base64url(secrets.token_bytes(32))
    code_challenge = _base64url(
        hashlib.sha256(code_verifier.encode()).digest()
    )

    state = secrets.token_urlsafe(16)

    _pkce_store[state] = code_verifier

    params = {
        "response_type": "code",
        "client_id": settings.CLIENT_ID,
        "redirect_uri": settings.REDIRECT_URI,
        "scope": "tweet.read tweet.write users.read offline.access",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"


def fetch_access_token(code: str, state: str):
    code_verifier = _pkce_store.pop(state)

    data = {
        "grant_type": "authorization_code",
        "client_id": settings.CLIENT_ID,
        "redirect_uri": settings.REDIRECT_URI,
        "code": code,
        "code_verifier": code_verifier,
    }

    r = requests.post(
        TOKEN_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        auth=(settings.CLIENT_ID, settings.CLIENT_SECRET),
    )

    r.raise_for_status()
    return r.json()
