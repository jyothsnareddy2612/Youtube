from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import threading

from app.workers.kafka_worker import start_kafka_consumer

app = FastAPI()


# ✅ CORS FIX (VERY IMPORTANT FOR HLS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ for dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🎥 Serve HLS videos
# maps: /hls/<video_id>/master.m3u8 → output/<video_id>/master.m3u8
app.mount("/hls", StaticFiles(directory="output"), name="hls")


# 🚀 Start Kafka in background
def start_kafka():
    try:
        print("🚀 Starting Kafka Consumer...")
        start_kafka_consumer()
    except Exception as e:
        print("❌ Kafka Error:", e)


@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=start_kafka)
    thread.daemon = True
    thread.start()


@app.get("/")
def root():
    return {"message": "Transcoder Service Running 🚀"}