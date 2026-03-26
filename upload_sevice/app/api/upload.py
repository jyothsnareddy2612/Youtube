import os
from fastapi import APIRouter, UploadFile, Form, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.upload_service import merge_chunks, save_video_metadata

router = APIRouter()

CHUNK_DIR = "videos/chunks"
os.makedirs(CHUNK_DIR, exist_ok=True)


@router.post("/upload-chunk")
async def upload_chunk(
    file: UploadFile,
    filename: str = Form(...),
    chunkIndex: int = Form(...),
    totalChunks: int = Form(...)
):
    chunk_filename = f"{filename}.part{chunkIndex}"
    chunk_path = os.path.join(CHUNK_DIR, chunk_filename)

    with open(chunk_path, "wb") as f:
        f.write(await file.read())

    return {"message": f"chunk {chunkIndex} uploaded"}


@router.post("/merge-chunks")
async def merge_chunks_api(
    request: Request,
    filename: str = Form(...),
    totalChunks: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    print("🔥 merge API hit")

    user = request.session.get("user")
    print("USER:", user)

    if not user:
        return {"error": "Login required"}

    final_path = await merge_chunks(filename, totalChunks)
    print("FINAL PATH:", final_path)

    video_id = await save_video_metadata(db, filename, final_path)
    print("VIDEO SAVED:", video_id)

    return {"video_id": video_id}