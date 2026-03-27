import os
from fastapi import APIRouter, UploadFile, Form, Request, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.upload_service import merge_chunks, save_video_metadata
from app.kafka.producer import KafkaProducerService

router = APIRouter()

producer = KafkaProducerService()

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
    db: Session = Depends(get_db)
):
    print("🔥 MERGE API HIT")

    user = request.session.get("user")

    if not user:
        return {"error": "Login required"}

    # merge file
    final_path = await merge_chunks(filename, totalChunks)
    print("📁 Final file:", final_path)

    # save DB
    video_id = save_video_metadata(db, filename, final_path)
    print("💾 Saved in DB:", video_id)

    # 🔥 SEND TO KAFKA (THIS WAS MISSING)
    file_path = os.path.abspath(final_path) 

    producer.send(
        topic="youtube_kafka",
        message={
            "video_id": video_id,
            "file_path": file_path
        }
    )

    print("📤 Sent to Kafka:", video_id)

    return {"video_id": video_id}