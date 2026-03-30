from app.db.database import SessionLocal
from app.models.video import Video
from app.services.opensearch_service import index_video

db = SessionLocal()

videos = db.query(Video).all()

print("Found:", len(videos))

for video in videos:
    print("Indexing:", video.title)
    index_video(video)

print("✅ Done")