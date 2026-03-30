from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.video import Video
from app.services.opensearch_service import index_video  # ✅ import once

router = APIRouter()


@router.post("/merge-chunks")
def merge_chunks(
    filename: str = Form(...),
    totalChunks: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        print("🔥 MERGE API HIT")

        # 👉 your existing merge logic here

        final_path = f"videos/raw/{filename}"

        # ✅ CREATE VIDEO OBJECT
        video = Video(
            id=str(uuid.uuid4()),
            title=filename,
            file_path=final_path,
            status="uploaded"
        )

        db.add(video)
        db.commit()
        db.refresh(video)

        print("💾 Saved in DB:", video.id)

        # 🔥 VERY IMPORTANT LINE (THIS WAS MISSING / WRONG PLACE)
        index_video(video)

        print("🔥 Indexed to OpenSearch")

        return {"message": "Upload successful", "video_id": video.id}

    except Exception as e:
        print("❌ Error:", str(e))
        return {"error": str(e)}