from fastapi import APIRouter, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
from app.core.config import GOOGLE_CLIENT_ID
from app.services.user_service import get_or_create_user
from app.core.security import create_access_token

router = APIRouter()

@router.post("/google")
async def google_login(data: dict):
    token = data.get("token")

    if not token:
        raise HTTPException(status_code=400, detail="Token missing")

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        user_data = {
            "email": idinfo.get("email"),
            "name": idinfo.get("name"),
            "picture": idinfo.get("picture"),
            "google_id": idinfo.get("sub"),
        }

        user = get_or_create_user(user_data)

        # ✅ Create JWT
        jwt_token = create_access_token({
            "email": user["email"]
        })

        return {
            "message": "User authenticated",
            "user": user_data,
            "access_token": jwt_token
        }

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")