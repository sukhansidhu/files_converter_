# bot/main.py
import logging
import os
from telegram.ext import Application
from bot.config import Config

# ✅ Handler setup functions
from bot.handlers.start import setup_start_handlers
from bot.handlers.menu import setup_menu_handlers
from bot.handlers.thumbnail_extractor import setup_thumbnail_handlers
from bot.handlers.caption_editor import setup_caption_handlers
from bot.handlers.progress_tracker import setup_progress_handlers
from bot.handlers.media_receiver import setup_media_handlers  # Handles video/audio/doc uploads

# ✅ Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    # ✅ Ensure required directories exist
    os.makedirs(Config.DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(Config.UPLOAD_PATH, exist_ok=True)
    os.makedirs(Config.THUMBNAIL_DIR, exist_ok=True)
    os.makedirs(Config.METADATA_DIR, exist_ok=True)

    # ✅ Initialize Telegram bot application
    application = Application.builder().token(Config.BOT_TOKEN).build()

    # ✅ Register all command/message handlers
    setup_start_handlers(application)
    setup_menu_handlers(application)
    setup_thumbnail_handlers(application)
    setup_caption_handlers(application)
    setup_progress_handlers(application)
    setup_media_handlers(application)

    # ✅ Start polling updates
    logger.info("🚀 Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
