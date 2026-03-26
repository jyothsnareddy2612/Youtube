import asyncio
from bson import ObjectId
from app.db.mongo import video_collection

async def process_video(event: dict):
    print("📥 Received event:", event)

    video_id = event["video_id"]
    file_path = event["file_path"]

    print(f"🎬 Processing file: {file_path}")

    # Update status → processing
    await video_collection.update_one(
        {"_id": ObjectId(video_id)},
        {"$set": {"status": "processing"}}
    )

    # Simulate processing
    await asyncio.sleep(5)

    # Update status → completed
    await video_collection.update_one(
        {"_id": ObjectId(video_id)},
        {"$set": {"status": "completed"}}
    )

    print("✅ Processing completed:", file_path)