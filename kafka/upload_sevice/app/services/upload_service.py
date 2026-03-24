from datetime import datetime
from app.db.mongo import video_collection
from app.kafka.producer import KafkaProducerService
from app.core.config import settings

producer = KafkaProducerService()

async def handle_video_upload(data: dict):
    # 1. Save to MongoDB
    video_doc = {
        "title": data["title"],
        "description": data["description"],
        "file_path": data["file_path"],
        "user_id": data["user_id"],
        "status": "uploaded",
        "created_at": datetime.utcnow()
    }

    result = await video_collection.insert_one(video_doc)

    # 2. Send Kafka Event
    event = {
        "video_id": str(result.inserted_id),
        "file_path": data["file_path"],
        "status": "uploaded"
    }

    producer.send(settings.KAFKA_TOPIC, event)

    return {"video_id": str(result.inserted_id)}