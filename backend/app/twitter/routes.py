from fastapi import APIRouter, Request
from app.twitter.oauth_service import fetch_access_token

router = APIRouter(prefix="/twitter", tags=["twitter"])

@router.get("/callback")
async def twitter_callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code or not state:
        return {"error": "Missing code or state"}

    token_data = fetch_access_token(code, state)
    return token_data
