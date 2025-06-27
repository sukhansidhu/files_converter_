from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# 🔘 Main menu layout
def main_menu_keyboard():
    buttons = [
        ["Thumbnail Extractor", "Caption And Buttons Editor", "Metadata Editor"],
        ["Media Forwarder", "Stream Remover", "Stream Extractor"],
        ["Video Trimmer", "Video Merger", "Remove Audio"],
        ["Merge 💷️ And 💷️", "Audio Converter", "Videos Splitter"],
        ["Screenshots", "Manual Shots", "Generate Sample"],
        ["Video To Audio", "Video Optimizer", "Subtitle Merger"],
        ["Video Converter", "Video Renamer", "Media Information"],
        ["Create Archive", "Cancel X"]
    ]

    keyboard = [
        [InlineKeyboardButton(text, callback_data=text) for text in row]
        for row in buttons
    ]

    return InlineKeyboardMarkup(keyboard)

# 📝 Caption/Buttons Editor layout
def caption_editor_keyboard():
    buttons = [
        ["Add Caption", "Remove Caption"],
        ["Add Button", "Remove Button"],
        ["Add New Caption", "Forward Button"],
        ["Back", "Cancel"]
    ]

    keyboard = [
        [
            InlineKeyboardButton(text, callback_data=f"caption_{text.replace(' ', '_')}")
            for text in row
        ]
        for row in buttons
    ]

    return InlineKeyboardMarkup(keyboard)

# 🎞️ Metadata stream selection layout
def metadata_editor_keyboard(streams):
    keyboard = []
    for stream in streams:
        stream_type = stream.get('type', '').capitalize()
        codec = stream.get('codec', 'Unknown')
        lang = stream.get('language', 'None')
        title = stream.get('title', 'None')
        short_title = (title[:10] + "...") if len(title) > 10 else title

        button_text = f"{stream_type} - {codec} - {lang} - {short_title}"
        callback_data = f"edit_stream_{stream['id']}"

        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])

    keyboard.append([
        InlineKeyboardButton("Edit All Streams", callback_data="edit_all_streams")
    ])
    keyboard.append([
        InlineKeyboardButton("Upload Video", callback_data="upload_video")
    ])
    keyboard.append([
        InlineKeyboardButton("❌ Cancel", callback_data="cancel_download")
    ])

    return InlineKeyboardMarkup(keyboard)

# 📊 Progress panel with cancel
def progress_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Progress", callback_data="show_progress")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_download")]
    ])

# ❌ Simple cancel option
def cancel_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_download")]
    ])
