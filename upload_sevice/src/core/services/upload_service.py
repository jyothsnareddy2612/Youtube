import os

from sqlalchemy.orm import Session

from src.data.models.postgres.video import Video

CHUNK_DIR = "videos/chunks"
RAW_DIR = "videos/raw"

os.makedirs(CHUNK_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)


async def merge_chunks(filename: str, total_chunks: int):
    final_path = os.path.join(RAW_DIR, filename)

    with open(final_path, "wb") as outfile:
        for index in range(total_chunks):
            chunk_path = os.path.join(CHUNK_DIR, f"{filename}.part{index}")
            with open(chunk_path, "rb") as infile:
                outfile.write(infile.read())

    return final_path


def save_video_metadata(db: Session, title: str, file_path: str):
    video = Video(title=title, file_path=file_path)
    db.add(video)
    db.commit()
    db.refresh(video)
    return video.id
