import asyncio
import os

import ffmpeg
from sqlalchemy.orm import Session

from src.data.clients.database import SessionLocal
from src.data.models.postgres.video import Video

BASE_OUTPUT_DIR = "output"


def update_video_status(
    video_id: str, status: str, master_path: str = None, error: str = None
):
    db: Session = SessionLocal()
    try:
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            print("Video not found in DB")
            return

        video.status = status
        if master_path:
            video.master_playlist = master_path
        if error:
            video.error = error
        db.commit()
    finally:
        db.close()


async def process_video(event: dict):
    video_id = event["video_id"]
    input_path = os.path.abspath(event["file_path"])

    await asyncio.to_thread(update_video_status, video_id, "processing")

    try:
        video_output_dir = os.path.join(BASE_OUTPUT_DIR, str(video_id))
        os.makedirs(video_output_dir, exist_ok=True)

        resolutions = [
            {"name": "180p", "resolution": "320x180", "video_bitrate": "500k", "audio_bitrate": "64k", "bandwidth": 676800},
            {"name": "480p", "resolution": "854x480", "video_bitrate": "1000k", "audio_bitrate": "128k", "bandwidth": 1353600},
            {"name": "720p", "resolution": "1280x720", "video_bitrate": "2500k", "audio_bitrate": "192k", "bandwidth": 3230400},
        ]

        variant_playlists = []
        for resolution in resolutions:
            resolution_dir = os.path.join(video_output_dir, resolution["name"])
            os.makedirs(resolution_dir, exist_ok=True)

            output_m3u8 = os.path.join(resolution_dir, "index.m3u8")
            segment_pattern = os.path.join(resolution_dir, "segment_%03d.ts")

            await asyncio.to_thread(
                run_ffmpeg, input_path, output_m3u8, segment_pattern, resolution
            )
            variant_playlists.append(
                {
                    "resolution": resolution["resolution"],
                    "bandwidth": resolution["bandwidth"],
                    "path": f"{resolution['name']}/index.m3u8",
                }
            )

        master_path = create_master_playlist(
            video_output_dir, variant_playlists, video_id
        )
        await asyncio.to_thread(update_video_status, video_id, "completed", master_path)
    except Exception as exc:
        await asyncio.to_thread(
            update_video_status, video_id, "failed", error=str(exc)
        )


def run_ffmpeg(input_path, output_m3u8, segment_pattern, resolution):
    (
        ffmpeg.input(input_path)
        .output(
            output_m3u8,
            **{
                "c:v": "libx264",
                "b:v": resolution["video_bitrate"],
                "c:a": "aac",
                "b:a": resolution["audio_bitrate"],
                "vf": f"scale={resolution['resolution']}",
                "f": "hls",
                "hls_time": 10,
                "hls_list_size": 0,
                "hls_segment_filename": segment_pattern,
            },
        )
        .run(overwrite_output=True)
    )


def create_master_playlist(video_output_dir, variants, video_id):
    master_path = os.path.join(video_output_dir, "master.m3u8")
    lines = ["#EXTM3U"]

    for variant in variants:
        lines.append(
            f"#EXT-X-STREAM-INF:BANDWIDTH={variant['bandwidth']},RESOLUTION={variant['resolution']}"
        )
        lines.append(variant["path"])

    with open(master_path, "w") as file_handle:
        file_handle.write("\n".join(lines))

    return f"{video_id}/master.m3u8"
