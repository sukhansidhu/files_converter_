import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from bot.utils.buttons import main_menu_keyboard
from bot.utils.helpers import get_file_name, get_file_size

logger = logging.getLogger(__name__)

# 🎬 Video Handler
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle both video messages and video documents
    if update.message.video:
        file = update.message.video
    elif update.message.document and "video" in update.message.document.mime_type:
        file = update.message.document
    else:
        await update.message.reply_text("❌ No valid video file found.")
        return

    filename = get_file_name(file)
    size = get_file_size(file.file_size)
    user_id = update.effective_user.id
    logger.info(f"[🎬 Video] From {user_id} - {filename} ({size})")

    await update.message.reply_text(
        f"🎬 **Video Received:** `{filename}`\n📦 **Size:** `{size}`\n\nChoose what to do next:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# 📁 Document Handler (non-video)
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Skip video documents (handled by video handler)
    if update.message.document and "video" in update.message.document.mime_type:
        return
        
    file = update.message.document
    if not file:
        return

    filename = get_file_name(file)
    size = get_file_size(file.file_size)
    user_id = update.effective_user.id
    logger.info(f"[📁 Document] From {user_id} - {filename} ({size})")

    await update.message.reply_text(
        f"📁 **File Received:** `{filename}`\n📦 **Size:** `{size}`\n\nSelect an action:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# 🎵 Audio Handler
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.audio
    if not file:
        return

    filename = get_file_name(file)
    size = get_file_size(file.file_size)
    user_id = update.effective_user.id
    logger.info(f"[🎵 Audio] From {user_id} - {filename} ({size})")

    await update.message.reply_text(
        f"🎵 **Audio Received:** `{filename}`\n📦 **Size:** `{size}`\n\nReady to edit or convert:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

# ✅ Register Handlers
def setup_media_handlers(app):
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.Document.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.Document.ALL & ~filters.Document.VIDEO, handle_document))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
