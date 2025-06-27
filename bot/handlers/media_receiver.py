# bot/handlers/media_receiver.py
import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

# ✅ Utilities
from bot.utils.buttons import main_menu_keyboard
from bot.utils.ffmpeg import extract_thumbnail, convert_video  # Optional, for future processing
from bot.utils.helpers import get_file_name, get_file_size

logger = logging.getLogger(__name__)

# 📥 Handle incoming videos (video message or video document)
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user
    file = update.message.video or update.message.document

    if not file:
        await update.message.reply_text("❌ No valid video file found.")
        return

    file_name = get_file_name(file)
    file_size = get_file_size(file.file_size)

    logger.info(f"📹 Video received from {user.id}: {file_name} ({file_size})")

    await update.message.reply_text(
        f"✅ Received your video: `{file_name}`\n📦 Size: {file_size}\n\nChoose what to do with it:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# 📂 Handle other documents (non-video)
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user
    file = update.message.document

    if not file:
        await update.message.reply_text("❌ No document file found.")
        return

    file_name = get_file_name(file)
    file_size = get_file_size(file.file_size)

    logger.info(f"📁 Document received from {user.id}: {file_name} ({file_size})")

    await update.message.reply_text(
        f"📁 Got your file: `{file_name}`\n📦 Size: {file_size}\n\nSelect an action:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# 🎵 Handle audio files
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user
    file = update.message.audio

    if not file:
        await update.message.reply_text("❌ No audio file found.")
        return

    file_name = get_file_name(file)
    file_size = get_file_size(file.file_size)

    logger.info(f"🎵 Audio received from {user.id}: {file_name} ({file_size})")

    await update.message.reply_text(
        f"🎵 Audio file: `{file_name}`\n📦 Size: {file_size}\n\nReady to convert or trim:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# 🧪 Catch-all for unexpected messages (for debugging)
async def catch_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        logger.warning("⚠️ Unhandled message type received")
        await update.message.reply_text("⚠️ This message type wasn't handled.")

# 🔁 Register all media handlers
def setup_media_handlers(app):
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))  # Normal videos
    app.add_handler(MessageHandler(filters.Document.VIDEO, handle_video))  # MP4/MKV as doc
    app.add_handler(MessageHandler(filters.Document.ALL & ~filters.Document.VIDEO, handle_document))  # All docs except video
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))  # Audio
    app.add_handler(MessageHandler(filters.ALL, catch_all))  # Catch-all
