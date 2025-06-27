import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from bot.utils.buttons import main_menu_keyboard
from bot.utils.helpers import get_file_name, get_file_size

logger = logging.getLogger(__name__)

# 📹 Video Handler (compressed or video document)
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.video or update.message.document
    if not file:
        await update.message.reply_text("❌ No valid video file found.")
        return

    filename = get_file_name(file)
    size = get_file_size(file.file_size)
    logger.info(f"📥 Video received: {filename} ({size})")

    await update.message.reply_text(
        f"🎬 Received: `{filename}`\n📦 Size: `{size}`\n\nChoose what to do next:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# 📁 Document Handler (non-video files)
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    if not file:
        await update.message.reply_text("❌ No document file found.")
        return

    filename = get_file_name(file)
    size = get_file_size(file.file_size)
    logger.info(f"📥 Document received: {filename} ({size})")

    await update.message.reply_text(
        f"📁 File: `{filename}`\n📦 Size: `{size}`\n\nSelect an action:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# 🎵 Audio Handler
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.audio
    if not file:
        await update.message.reply_text("❌ No audio file found.")
        return

    filename = get_file_name(file)
    size = get_file_size(file.file_size)
    logger.info(f"🎵 Audio received: {filename} ({size})")

    await update.message.reply_text(
        f"🎵 Audio: `{filename}`\n📦 Size: `{size}`\n\nReady to edit:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# 🧠 Setup function
def setup_media_handlers(app):
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))  # Normal videos
    app.add_handler(MessageHandler(filters.Document.VIDEO, handle_video))  # MP4/MKV as doc
    app.add_handler(MessageHandler(filters.Document.ALL & ~filters.Document.VIDEO, handle_document))  # All docs except video
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))  # Audio
