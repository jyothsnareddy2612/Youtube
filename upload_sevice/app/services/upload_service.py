import os
from sqlalchemy.orm import Session   # ✅ FIXED
from app.models.video import Video

CHUNK_DIR = "videos/chunks"
RAW_DIR = "videos/raw"

os.makedirs(CHUNK_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)


# ✅ keep async (file IO is fine)
async def merge_chunks(filename: str, total_chunks: int):
    final_path = os.path.join(RAW_DIR, filename)

    with open(final_path, "wb") as outfile:
        for i in range(total_chunks):
            chunk_path = os.path.join(CHUNK_DIR, f"{filename}.part{i}")
            with open(chunk_path, "rb") as infile:
                outfile.write(infile.read())

    return final_path


# 🔥 IMPORTANT: make this SYNC
def save_video_metadata(db: Session, title: str, file_path: str):
    video = Video(title=title, file_path=file_path)

    db.add(video)
    db.commit()        # ✅ NO await
    db.refresh(video)  # ✅ NO await

    return video.id