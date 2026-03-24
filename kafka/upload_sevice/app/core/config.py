import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")

    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_USERNAME: str = os.getenv("KAFKA_USERNAME")
    KAFKA_PASSWORD: str = os.getenv("KAFKA_PASSWORD")
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC")
    KAFKA_CA_PATH = os.getenv("KAFKA_CA_PATH", "./ca.pem")

settings = Settings()