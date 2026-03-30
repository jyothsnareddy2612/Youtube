import asyncio

from src.config.settings import settings
from src.core.services.transcoder_service import process_video
from src.handlers.http_clients.kafka_consumer import KafkaConsumerService

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

consumer = KafkaConsumerService(
    topic=settings.KAFKA_TOPIC,
    group_id="transcoder-group",
)


def handler(data):
    loop.run_until_complete(process_video(data))


def start_kafka_consumer():
    consumer.start(handler)
