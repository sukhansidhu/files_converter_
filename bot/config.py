import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # 🔐 Telegram bot token (required)
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set. Please define it in your .env file or environment variables.")

    # 📁 Directory paths
    DOWNLOAD_PATH = "downloads"
    UPLOAD_PATH = "uploads"
    THUMBNAIL_DIR = "thumbnails"
    METADATA_DIR = "metadata"

    # ⚙️ Limits and bot behavior
    MAX_TITLE_LENGTH = 10
    MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2 GB

    # 🔒 Allowed users (optional)
    ALLOWED_USERS = list(
        map(int, os.getenv("ALLOWED_USERS", "").split(","))
    ) if os.getenv("ALLOWED_USERS") else []

    # 🛠 FFmpeg binary path
    FFMPEG_PATH = "ffmpeg"
