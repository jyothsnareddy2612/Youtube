import os
import asyncio
import ffmpeg
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.video import Video

BASE_OUTPUT_DIR = "output"


# ✅ DB helper
def update_video_status(video_id: str, status: str, master_path: str = None, error: str = None):
    db: Session = SessionLocal()

    try:
        video = db.query(Video).filter(Video.id == video_id).first()

        if not video:
            print("❌ Video not found in DB")
            return

        video.status = status

        if master_path:
            video.master_playlist = master_path

        if error:
            video.error = error

        db.commit()

    finally:
        db.close()


# 🎬 MAIN FUNCTION
async def process_video(event: dict):
    print("📥 Received event:", event)

    video_id = event["video_id"]
    input_path = os.path.abspath(event["file_path"])  # ✅ fix path

    print(f"🎬 Processing file: {input_path}")

    # 1️⃣ processing
    await asyncio.to_thread(update_video_status, video_id, "processing")

    try:
        # 2️⃣ output folder
        video_output_dir = os.path.join(BASE_OUTPUT_DIR, str(video_id))
        os.makedirs(video_output_dir, exist_ok=True)

        resolutions = [
            {"name": "180p", "resolution": "320x180", "video_bitrate": "500k", "audio_bitrate": "64k", "bandwidth": 676800},
            {"name": "480p", "resolution": "854x480", "video_bitrate": "1000k", "audio_bitrate": "128k", "bandwidth": 1353600},
            {"name": "720p", "resolution": "1280x720", "video_bitrate": "2500k", "audio_bitrate": "192k", "bandwidth": 3230400},
        ]

        variant_playlists = []

        for res in resolutions:
            res_dir = os.path.join(video_output_dir, res["name"])
            os.makedirs(res_dir, exist_ok=True)

            output_m3u8 = os.path.join(res_dir, "index.m3u8")
            segment_pattern = os.path.join(res_dir, "segment_%03d.ts")

            print(f"⚙️ Processing {res['name']}...")

            await asyncio.to_thread(
                run_ffmpeg,
                input_path,
                output_m3u8,
                segment_pattern,
                res,
            )

            variant_playlists.append({
                "resolution": res["resolution"],
                "bandwidth": res["bandwidth"],
                "path": f"{res['name']}/index.m3u8",
            })

            print(f"✅ Done {res['name']}")

        # ✅ CREATE MASTER PLAYLIST (FIXED)
        master_path = create_master_playlist(video_output_dir, variant_playlists, video_id)

        # 6️⃣ completed
        await asyncio.to_thread(
            update_video_status,
            video_id,
            "completed",
            master_path
        )

        print("🎉 Processing completed:", input_path)

    except Exception as e:
        print("❌ Error:", str(e))

        await asyncio.to_thread(
            update_video_status,
            video_id,
            "failed",
            error=str(e)
        )


# ⚙️ FFmpeg
def run_ffmpeg(input_path, output_m3u8, segment_pattern, res):
    (
        ffmpeg
        .input(input_path)
        .output(
            output_m3u8,
            **{
                "c:v": "libx264",
                "b:v": res["video_bitrate"],
                "c:a": "aac",
                "b:a": res["audio_bitrate"],
                "vf": f"scale={res['resolution']}",
                "f": "hls",
                "hls_time": 10,
                "hls_list_size": 0,
                "hls_segment_filename": segment_pattern,
            }
        )
        .run(overwrite_output=True)
    )


# 📄 MASTER PLAYLIST (🔥 FINAL FIX)
def create_master_playlist(video_output_dir, variants, video_id):
    master_path = os.path.join(video_output_dir, "master.m3u8")

    lines = ["#EXTM3U"]

    for v in variants:
        lines.append(
            f"#EXT-X-STREAM-INF:BANDWIDTH={v['bandwidth']},RESOLUTION={v['resolution']}"
        )
        lines.append(v["path"])

    with open(master_path, "w") as f:
        f.write("\n".join(lines))

    print("📄 Master playlist created")

    # ✅ ONLY RELATIVE PATH (NO output/)
    return f"{video_id}/master.m3u8"