from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.video import Video

router = APIRouter()


@router.get("/videos")
def get_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).all()   # ✅ NO async

    return videos