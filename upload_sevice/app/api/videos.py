from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.models.video import Video

router = APIRouter()

@router.get("/videos")
async def get_videos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Video))
    videos = result.scalars().all()

    return [
        {
            "id": v.id,
            "title": v.title,
            "file_path": v.file_path
        }
        for v in videos
    ]