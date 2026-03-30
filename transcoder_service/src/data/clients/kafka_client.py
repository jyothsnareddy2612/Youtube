from confluent_kafka import Consumer, Producer

from src.config.settings import settings


def get_kafka_config():
    return {
        "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
        "security.protocol": "SASL_SSL",
        "sasl.mechanism": "PLAIN",
        "sasl.username": settings.KAFKA_USERNAME,
        "sasl.password": settings.KAFKA_PASSWORD,
        "ssl.ca.location": settings.KAFKA_CA_PATH,
    }


def create_producer():
    return Producer(get_kafka_config())


def create_consumer(group_id: str):
    config = get_kafka_config()
    config.update({"group.id": group_id, "auto.offset.reset": "earliest"})
    return Consumer(config)
