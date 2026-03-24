import json
from app.kafka.kafka_config import create_consumer

class KafkaConsumerService:
    def __init__(self, topic: str, group_id: str):
        self.consumer = create_consumer(group_id)
        self.topic = topic

    def start(self, handler):
        self.consumer.subscribe([self.topic])

        print("🚀 Kafka consumer started...")

        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                if msg.error():
                    print(f"❌ Error: {msg.error()}")
                    continue

                data = json.loads(msg.value().decode("utf-8"))
                handler(data)

        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()