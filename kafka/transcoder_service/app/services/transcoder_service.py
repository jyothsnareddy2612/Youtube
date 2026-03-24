import time
from bson import ObjectId
from app.db.mongo import video_collection

async def process_video(event: dict):
    print("🎬 Processing video:", event)

    video_id = event["video_id"]

    # 1. Mark as processing
    await video_collection.update_one(
        {"_id": ObjectId(video_id)},
        {"$set": {"status": "processing"}}
    )

    # 2. Simulate processing
    time.sleep(5)  # ⚠️ blocking (we'll fix later)

    # 3. Mark as completed
    await video_collection.update_one(
        {"_id": ObjectId(video_id)},
        {"$set": {"status": "completed"}}
    )

    print("✅ Processing completed:", video_id)