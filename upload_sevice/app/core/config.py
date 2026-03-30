import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # 🔹 PostgreSQL (ONLY DB now)
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # 🔹 Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_USERNAME: str = os.getenv("KAFKA_USERNAME")
    KAFKA_PASSWORD: str = os.getenv("KAFKA_PASSWORD")
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC")
    KAFKA_CA_PATH: str = os.getenv("KAFKA_CA_PATH", "./ca.pem")

    # 🔹 Google OAuth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI: str = os.getenv("REDIRECT_URI")
    SESSION_SECRET: str = os.getenv("SESSION_SECRET", "secret")
    OPENSEARCH_HOST: str = os.getenv("OPENSEARCH_HOST")
    OPENSEARCH_USER: str = os.getenv("OPENSEARCH_USER")
    OPENSEARCH_PASSWORD: str = os.getenv("OPENSEARCH_PASSWORD")

settings = Settings()