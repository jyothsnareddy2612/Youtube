import asyncio
from app.kafka.consumer import KafkaConsumerService
from app.core.config import settings
from app.services.transcoder_service import process_video

consumer = KafkaConsumerService(
    topic=settings.KAFKA_TOPIC,
    group_id="transcoder-group"
)

def start_kafka_consumer():
    def handler(data):
        print("📥 Received from Kafka:", data)

        # Run async function inside sync loop
        asyncio.run(process_video(data))

    consumer.start(handler)