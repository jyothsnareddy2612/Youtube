from fastapi import APIRouter, UploadFile, File, Form
from app.database.mongo import users_collection
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "app/uploads"

@router.post("/upload-profile")
async def upload_profile(
    file: UploadFile = File(...),
    email: str = Form(...)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # update user profile picture
    users_collection.update_one(
        {"email": email},
        {"$set": {"picture": file_path}}
    )

    return {
        "message": "Profile updated",
        "file_path": file_path
    }