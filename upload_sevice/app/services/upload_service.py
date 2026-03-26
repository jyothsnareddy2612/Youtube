import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.video import Video

CHUNK_DIR = "videos/chunks"
RAW_DIR = "videos/raw"

os.makedirs(CHUNK_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)


async def merge_chunks(filename: str, total_chunks: int):
    final_path = os.path.join(RAW_DIR, filename)

    with open(final_path, "wb") as outfile:
        for i in range(total_chunks):
            chunk_path = os.path.join(CHUNK_DIR, f"{filename}.part{i}")
            with open(chunk_path, "rb") as infile:
                outfile.write(infile.read())

    return final_path


async def save_video_metadata(db: AsyncSession, title: str, file_path: str):
    video = Video(title=title, file_path=file_path)
    db.add(video)
    await db.commit()
    await db.refresh(video)
    return video.id