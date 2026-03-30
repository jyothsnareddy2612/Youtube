import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "youtube-service")
    ENV: str = os.getenv("ENV", "development")
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_USERNAME: str = os.getenv("KAFKA_USERNAME")
    KAFKA_PASSWORD: str = os.getenv("KAFKA_PASSWORD")
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "transcode")
    KAFKA_CA_PATH: str = os.getenv("KAFKA_CA_PATH", "./ca.pem")
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    def validate(self):
        required_fields = {
            "KAFKA_BOOTSTRAP_SERVERS": self.KAFKA_BOOTSTRAP_SERVERS,
            "KAFKA_USERNAME": self.KAFKA_USERNAME,
            "KAFKA_PASSWORD": self.KAFKA_PASSWORD,
        }
        missing = [key for key, value in required_fields.items() if not value]
        if missing:
            raise ValueError(f"Missing required env variables: {', '.join(missing)}")


settings = Settings()
settings.validate()
