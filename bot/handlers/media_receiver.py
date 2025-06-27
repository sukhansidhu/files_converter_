# bot/handlers/media_receiver.py

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

# ✅ Import buttons
from bot.utils.buttons import main_menu_keyboard

# ✅ If you want to use FFmpeg functions or helpers later
from bot.utils.ffmpeg import extract_thumbnail, convert_video  # (example names)
from bot.utils.helpers import get_file_name, format_file_size     # (example names)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Received your video! Now choose what to do with it:",
        reply_markup=main_menu_keyboard()
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📁 Got your file. Now select what to do:",
        reply_markup=main_menu_keyboard()
    )

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Audio received. Ready to convert or trim.",
        reply_markup=main_menu_keyboard()
    )

def setup_media_handlers(app):
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.Document.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.Document.ALL & ~filters.Document.VIDEO, handle_document))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
