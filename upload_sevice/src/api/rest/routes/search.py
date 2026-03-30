from fastapi import APIRouter

from src.core.services.search_service import search_videos

router = APIRouter()


@router.get("/search")
def search(query: str):
    try:
        return search_videos(query)
    except Exception as exc:
        print("Search Error:", str(exc))
        return []
