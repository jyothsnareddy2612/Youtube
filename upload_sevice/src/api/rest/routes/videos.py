from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.data.clients.database import get_db
from src.data.repositories.video_repository import get_all_videos

router = APIRouter()


@router.get("/videos")
def get_videos(db: Session = Depends(get_db)):
    return get_all_videos(db)
