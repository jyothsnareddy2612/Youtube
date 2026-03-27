import asyncio
from app.kafka.consumer import KafkaConsumerService
from app.core.config import settings
from app.services.transcoder_service import process_video

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

consumer = KafkaConsumerService(
    topic=settings.KAFKA_TOPIC,
    group_id="transcoder-group"
)


def handler(data):
    print("📥 Data from Kafka:", data)

    # 🔥 FIX: run async properly
    loop.run_until_complete(process_video(data))


def start_kafka_consumer():
    print("🚀 Starting Transcoder Service...")
    print("👀 Waiting for Kafka messages...")

    consumer.start(handler)