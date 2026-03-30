from sqlalchemy.orm import Session

from src.data.models.postgres.video import Video


def get_all_videos(db: Session):
    return db.query(Video).all()
