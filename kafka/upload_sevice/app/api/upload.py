from fastapi import APIRouter, UploadFile, File, Form
import os
from app.services.upload_service import handle_video_upload

router = APIRouter()

UPLOAD_DIR = "videos/raw"

@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    user_id: str = Form(...)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file locally
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Convert to absolute path (IMPORTANT)
    abs_path = os.path.abspath(file_path)

    data = {
        "title": title,
        "description": description,
        "file_path": abs_path,
        "user_id": user_id
    }

    result = await handle_video_upload(data)

    return {
        "message": "Video uploaded successfully",
        "data": result
    }