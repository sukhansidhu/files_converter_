import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from bot.utils.buttons import main_menu_keyboard
from bot.utils.helpers import get_file_name, get_file_size

logger = logging.getLogger(__name__)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Try to get video from different sources
        if update.message.video:
            file = update.message.video
            file_type = "video message"
        elif update.message.document and update.message.document.mime_type.startswith('video/'):
            file = update.message.document
            file_type = "video document"
        else:
            logger.warning("Received non-video media as video")
            return

        filename = get_file_name(file)
        size = get_file_size(file.file_size)
        user_id = update.effective_user.id
        
        logger.info(f"[🎬 VIDEO] From {user_id} - {filename} ({size}) - Type: {file_type}")

        await update.message.reply_text(
            f"🎬 **Video Received:** `{filename}`\n📦 **Size:** `{size}`\n\nChoose what to do next:",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard()
        )
    except Exception as e:
        logger.error(f"Video handler error: {str(e)}")
        await update.message.reply_text("❌ Error processing your video. Please try again.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Skip video documents (handled by video handler)
        if update.message.document and update.message.document.mime_type.startswith('video/'):
            return
            
        file = update.message.document
        if not file:
            return

        filename = get_file_name(file)
        size = get_file_size(file.file_size)
        user_id = update.effective_user.id
        logger.info(f"[📁 DOCUMENT] From {user_id} - {filename} ({size})")

        await update.message.reply_text(
            f"📁 **File Received:** `{filename}`\n📦 **Size:** `{size}`\n\nSelect an action:",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard()
        )
    except Exception as e:
        logger.error(f"Document handler error: {str(e)}")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = update.message.audio
        if not file:
            return

        filename = get_file_name(file)
        size = get_file_size(file.file_size)
        user_id = update.effective_user.id
        logger.info(f"[🎵 AUDIO] From {user_id} - {filename} ({size})")

        await update.message.reply_text(
            f"🎵 **Audio Received:** `{filename}`\n📦 **Size:** `{size}`\n\nReady to edit or convert:",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard()
        )
    except Exception as e:
        logger.error(f"Audio handler error: {str(e)}")

def setup_media_handlers(app):
    # Register with high priority (group 1)
    app.add_handler(MessageHandler(filters.VIDEO, handle_video), group=1)
    app.add_handler(MessageHandler(filters.Document.VIDEO | filters.Document.MimeType("video/*"), handle_video), group=1)
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document), group=1)
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio), group=1)
    logger.info("Media handlers registered with high priority")
