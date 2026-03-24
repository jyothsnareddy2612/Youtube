from fastapi import APIRouter
from app.models.video import VideoUploadRequest
from app.services.upload_service import handle_video_upload

router = APIRouter()

@router.post("/upload")
async def upload_video(payload: VideoUploadRequest):
    result = await handle_video_upload(payload.dict())
    return {
        "message": "Video uploaded successfully",
        "data": result
    }