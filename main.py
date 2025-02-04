from fastapi import FastAPI, Query, HTTPException, UploadFile, File
from typing import List, Optional
import numpy as np
from typing import Union
import pywt
import subprocess
import os
import cv2
from tempfile import NamedTemporaryFile
import shutil
import tempfile
import uuid


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
       
       
       
@app.get("/api/cut_video")

async def cut_video(file: UploadFile = File(...)):
    """
    Uploads a video, trims it to 1 minute, and packages it as:
    a) HLS (MP4 container, H.264, AAC)
    b) MPEG-DASH (MKV container, VP9, AAC)
    """
    try:
        # Create a temporary directory for processing
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, "input.mp4")
        cut_video_path = os.path.join(temp_dir, "cut_video.mp4")
        hls_output_path = os.path.join(OUTPUT_DIR, "output.m3u8")
        dash_output_path = os.path.join(OUTPUT_DIR, "output.mpd")

        # Save uploaded file to temp location
        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Step 1: Trim the video to 1 minute
        subprocess.run(
            ["ffmpeg", "-i", input_path, "-t", "60", "-c", "copy", cut_video_path],
            check=True
        )

        # Step 2: Package as HLS (MP4, H.264, AAC)
        subprocess.run(
            [
                "ffmpeg",
                "-i", cut_video_path,
                "-c:v", "libx264",
                "-b:v", "2000k",
                "-c:a", "aac",
                "-b:a", "128k",
                "-hls_time", "10",
                "-hls_playlist_type", "vod",
                "-f", "hls",
                hls_output_path,
            ],
            check=True
        )

        # Step 3: Package as MPEG-DASH (MKV, VP9, AAC)
        subprocess.run(
            [
                "ffmpeg",
                "-i", cut_video_path,
                "-c:v", "libvpx-vp9",
                "-b:v", "2000k",
                "-c:a", "aac",
                "-b:a", "128k",
                "-f", "dash",
                dash_output_path,
            ],
            check=True
        )

        return {
            "message": "Video processing complete!",
            "hls_output": hls_output_path,
            "dash_output": dash_output_path,
        }

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"FFmpeg error: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing video: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)     
        
