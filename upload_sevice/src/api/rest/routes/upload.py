import os

from fastapi import APIRouter, Depends, Form, Request, UploadFile
from sqlalchemy.orm import Session

from src.core.services.indexing_service import index_video
from src.core.services.upload_service import merge_chunks, save_video_metadata
from src.data.clients.database import get_db
from src.data.models.postgres.video import Video
from src.handlers.http_clients.kafka_producer import KafkaProducerService

router = APIRouter()
producer = KafkaProducerService()
CHUNK_DIR = "videos/chunks"
os.makedirs(CHUNK_DIR, exist_ok=True)


@router.post("/upload-chunk")
async def upload_chunk(
    file: UploadFile,
    filename: str = Form(...),
    chunkIndex: int = Form(...),
    totalChunks: int = Form(...),
):
    chunk_filename = f"{filename}.part{chunkIndex}"
    chunk_path = os.path.join(CHUNK_DIR, chunk_filename)

    with open(chunk_path, "wb") as file_handle:
        file_handle.write(await file.read())

    return {"message": f"chunk {chunkIndex} uploaded"}


@router.post("/merge-chunks")
async def merge_chunks_api(
    request: Request,
    filename: str = Form(...),
    totalChunks: int = Form(...),
    db: Session = Depends(get_db),
):
    user = request.session.get("user")
    if not user:
        return {"error": "Login required"}

    final_path = await merge_chunks(filename, totalChunks)
    video_id = save_video_metadata(db, filename, final_path)
    video = db.query(Video).filter(Video.id == video_id).first()

    if video:
        index_video(video)

    producer.send(
        topic="youtube_kafka",
        message={"video_id": video_id, "file_path": os.path.abspath(final_path)},
    )

    return {"video_id": video_id}
