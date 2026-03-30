from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import requests
from app.core.config import settings

router = APIRouter()


@router.get("/login")
def login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid email profile"
    )
    return RedirectResponse(google_auth_url)


@router.get("/callback")
def callback(request: Request, code: str):
    token_url = "https://oauth2.googleapis.com/token"

    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(token_url, data=token_data).json()
    access_token = token_response.get("access_token")

    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    # ✅ STORE SESSION CORRECTLY
    request.session["user"] = {
        "name": user_info.get("name"),
        "email": user_info.get("email"),
        "picture": user_info.get("picture"),
    }

    return RedirectResponse("http://localhost:3000")


@router.get("/me")
def get_user(request: Request):
    return request.session.get("user", None)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out"}