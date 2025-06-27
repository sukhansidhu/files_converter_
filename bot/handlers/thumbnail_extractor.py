import os
import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, CallbackQueryHandler, filters

from bot.config import Config
from bot.utils.ffmpeg import extract_thumbnail
from bot.utils.buttons import cancel_keyboard

logger = logging.getLogger(__name__)

# Step 1: Ask user to send a video
async def handle_thumbnail_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🎬 Please send a video to extract a thumbnail:",
        reply_markup=cancel_keyboard()
    )
    context.user_data['expecting'] = 'thumbnail_video'

# Step 2: Handle the incoming video and extract thumbnail
async def process_thumbnail_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    if user_data.get('expecting') != 'thumbnail_video':
        return

    video = update.message.video
    if not video:
        await update.message.reply_text("⚠️ Please send a valid video file.")
        return

    try:
        # Ensure directories exist
        os.makedirs(Config.DOWNLOAD_PATH, exist_ok=True)
        os.makedirs(Config.THUMBNAIL_DIR, exist_ok=True)

        # Download the video
        video_file = await video.get_file()
        video_path = os.path.join(Config.DOWNLOAD_PATH, f"{video.file_id}.mp4")
        await video_file.download_to_drive(video_path)

        # Extract thumbnail
        thumbnail_path = extract_thumbnail(video_path, Config.THUMBNAIL_DIR)

        if thumbnail_path and os.path.exists(thumbnail_path):
            with open(thumbnail_path, 'rb') as thumb:
                await update.message.reply_photo(photo=thumb, caption="✅ Here's your thumbnail!")
        else:
            await update.message.reply_text("❌ Failed to extract thumbnail. Try a different video.")
    except Exception as e:
        logger.error(f"Thumbnail extraction failed: {e}")
        await update.message.reply_text("🚫 An error occurred while processing the video.")
    finally:
        user_data.pop('expecting', None)

# Step 3: Register handlers
def setup_thumbnail_handlers(application):
    application.add_handler(CallbackQueryHandler(handle_thumbnail_request, pattern="^Thumbnail Extractor$"))
    application.add_handler(MessageHandler(filters.VIDEO & ~filters.COMMAND, process_thumbnail_video))
