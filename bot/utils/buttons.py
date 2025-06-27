# bot/handlers/menu.py

from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = query.data  # this is the callback_data (e.g., "Video Converter")

    # Now handle different tools
    if action == "Video Converter":
        await query.edit_message_text("🔄 Starting video conversion...")
        # Placeholder: integrate ffmpeg here
    elif action == "Thumbnail Extractor":
        await query.edit_message_text("🖼 Extracting thumbnail...")
    elif action == "Caption And Buttons Editor":
        await query.edit_message_text("📝 Caption and button editor opened.")
    elif action == "Metadata Editor":
        await query.edit_message_text("📄 Editing metadata streams...")
    elif action == "Cancel X":
        await query.edit_message_text("❌ Cancelled.")
    else:
        await query.edit_message_text(f"⚙️ You clicked: {action}")

def setup_menu_handlers(app):
    app.add_handler(CallbackQueryHandler(main_menu_callback))
