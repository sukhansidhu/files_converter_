# bot/handlers/media_receiver.py

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Received your video! Now choose what to do with it:")
    # Show the main menu or tools (e.g., using main_menu_keyboard)
    # await update.message.reply_text("Choose an action:", reply_markup=main_menu_keyboard())

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📁 Got your file. Now select what to do.")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Audio received. Ready to convert or trim.")

def setup_media_handlers(app):
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.Document.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
