# bot/handlers/media_receiver.py
import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

# ✅ Utilities
from bot.utils.buttons import main_menu_keyboard
from bot.utils.ffmpeg import extract_thumbnail, convert_video  # Optional, for future processing
from bot.utils.helpers import get_file_name, get_file_size     # You already have these

logger = logging.getLogger(__name__)

# 📥 Handle incoming videos
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    file = update.message.video or update.message.document

    file_name = get_file_name(file)
    file_size = get_file_size(file.file_size)

    logger.info(f"📹 Video received from {user.id}: {file_name} ({file_size})")

    await update.message.reply_text(
        f"✅ Received your video: `{file_name}`\nSize: {file_size}\n\nChoose what to do with it:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# 📂 Handle other documents (non-video)
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    file = update.message.document

    file_name = get_file_name(file)
    file_size = get_file_size(file.file_size)

    logger.info(f"📁 Document received from {user.id}: {file_name} ({file_size})")

    await update.message.reply_text(
        f"📁 Got your file: `{file_name}`\nSize: {file_size}\n\nSelect an action:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# 🎵 Handle audio files
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    file = update.message.audio

    file_name = get_file_name(file)
    file_size = get_file_size(file.file_size)

    logger.info(f"🎵 Audio received from {user.id}: {file_name} ({file_size})")

    await update.message.reply_text(
        f"🎵 Audio file: `{file_name}`\nSize: {file_size}\n\nReady to convert or trim:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# 🔁 Register these handlers
def setup_media_handlers(app):
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.Document.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.Document.ALL & ~filters.Document.VIDEO, handle_document))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
