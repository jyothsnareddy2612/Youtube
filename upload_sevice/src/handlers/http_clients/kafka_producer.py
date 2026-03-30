import json

from src.data.clients.kafka_client import create_producer


class KafkaProducerService:
    def __init__(self):
        self.producer = create_producer()

    def delivery_report(self, err, msg):
        if err:
            print(f"Delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def send(self, topic: str, message: dict):
        try:
            self.producer.produce(
                topic=topic,
                value=json.dumps(message),
                callback=self.delivery_report,
            )
            self.producer.flush()
        except Exception as exc:
            print(f"Kafka Producer Error: {exc}")
