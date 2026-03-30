import threading

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.middleware.cors import register_cors
from src.control.agents.kafka_worker import start_kafka_consumer

app = FastAPI()
register_cors(app)
app.mount("/hls", StaticFiles(directory="output"), name="hls")


def start_kafka():
    try:
        start_kafka_consumer()
    except Exception as exc:
        print("Kafka Error:", exc)


@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=start_kafka)
    thread.daemon = True
    thread.start()


@app.get("/")
def root():
    return {"message": "Transcoder Service Running"}
