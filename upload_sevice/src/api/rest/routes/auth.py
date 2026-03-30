from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from src.config.settings import settings
from src.handlers.http_clients.google_oauth import exchange_code_for_user

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
    user_info = exchange_code_for_user(
        {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.REDIRECT_URI,
            "grant_type": "authorization_code",
        }
    )

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
