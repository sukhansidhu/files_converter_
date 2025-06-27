import os
import subprocess
import logging
from bot.config import Config

logger = logging.getLogger(__name__)

# 📸 Extract one thumbnail frame from video
def extract_thumbnail(video_path, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "thumbnail.jpg")
        cmd = [
            Config.FFMPEG_PATH,
            "-i", video_path,
            "-ss", "00:00:01",   # seek to 1 second
            "-vframes", "1",
            "-q:v", "2",         # quality
            output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except Exception as e:
        logger.error(f"Thumbnail extraction failed: {e}")
        return None

# 🏷️ Edit metadata of video/audio/subtitle streams
def edit_metadata(input_path, output_path, metadata):
    try:
        cmd = [Config.FFMPEG_PATH, "-i", input_path, "-map", "0"]

        for i, meta in enumerate(metadata):
            if meta.get('title'):
                cmd += ["-metadata:s:{}:{}".format(meta['type'][0], i), f"title={meta['title']}"]
            if meta.get('language'):
                cmd += ["-metadata:s:{}:{}".format(meta['type'][0], i), f"language={meta['language']}"]

        cmd += ["-c", "copy", output_path]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except Exception as e:
        logger.error(f"Metadata editing failed: {e}")
        return None

# 🎬 Merge multiple videos into one
def merge_videos(video_paths, output_path):
    try:
        os.makedirs(Config.UPLOAD_PATH, exist_ok=True)
        list_path = os.path.join(Config.UPLOAD_PATH, "filelist.txt")
        with open(list_path, "w") as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")
        
        cmd = [
            Config.FFMPEG_PATH,
            "-f", "concat",
            "-safe", "0",
            "-i", list_path,
            "-c", "copy",
            output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except Exception as e:
        logger.error(f"Video merging failed: {e}")
        return None

# ✂️ Trim a video
def trim_video(input_path, output_path, start_time, end_time):
    try:
        cmd = [
            Config.FFMPEG_PATH,
            "-i", input_path,
            "-ss", str(start_time),
            "-to", str(end_time),
            "-c", "copy",
            output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except Exception as e:
        logger.error(f"Video trimming failed: {e}")
        return None

# 🔄 Convert video format
def convert_video(input_path, output_path):
    try:
        cmd = [
            Config.FFMPEG_PATH,
            "-i", input_path,
            "-preset", "fast",  # speeds up processing
            output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except Exception as e:
        logger.error(f"Video conversion failed: {e}")
        return None
