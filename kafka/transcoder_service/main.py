from app.workers.kafka_worker import start_kafka_consumer

if __name__ == "__main__":
    print("🚀 Starting Transcoder Service...")
    start_kafka_consumer()