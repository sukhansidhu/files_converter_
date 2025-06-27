# 🎬 Telegram Media Toolkit Bot

A powerful, modular Telegram bot built with `python-telegram-bot` and `FFmpeg` to process videos, audio, captions, thumbnails, metadata, and more. Designed for advanced users and creators who want an all-in-one video processing solution via Telegram.

---

## 🚀 Features

✅ Media Processing Tools:
- 📸 Thumbnail Extractor
- 📝 Caption and Button Editor
- 🧾 Metadata Stream Editor (video/audio/subtitle)
- 🔊 Remove or Add Audio
- ✂️ Video Trimmer
- 🎞️ Video Merger
- 🎥 Stream Extractor / Remover
- 🔄 Video Converter (MP4, MKV, etc.)
- 🎧 Audio Converter
- 🎛️ Subtitle Merger
- 🧠 Media Info Inspector
- 🗜️ Archive Creator (coming soon)

💬 Interactive UI:
- Inline buttons with real-time updates
- Progress feedback (download %, speed, ETA)
- Cancel or resume tasks

🔧 Modular Codebase:
- Easy to extend with new tools
- Clean handler separation
- Environment-based configuration

---

## 📂 Project Structure

## ⚙️ Installation

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/media_toolkit_bot.git
cd media_toolkit_bot

2. Install Requirements

pip install -r requirements.txt

3. Configure Environment

Rename .env.example to .env and fill in:

BOT_TOKEN=your_telegram_bot_token
FFMPEG_PATH=/usr/bin/ffmpeg
DOWNLOAD_PATH=downloads
UPLOAD_PATH=uploads
THUMBNAIL_DIR=thumbnails
METADATA_DIR=metadata


---

🐳 Optional: Run via Docker

Build & Run the bot in a container:

docker build -t media-bot .
docker run -d --env-file .env media-bot


---

▶️ Run the Bot

python bot/main.py

The bot should now be live and responding on Telegram.


---

👨‍💻 Development Notes

Built using python-telegram-bot v20+ with async support.

Uses FFmpeg for all media operations.

Uses pymediainfo for reading metadata.



---

🛠️ Contributing

PRs are welcome! Please fork and submit via feature branches.


---

📝 License

This project is licensed under the MIT License.


---

🌐 Credits

python-telegram-bot

FFmpeg

pymediainfo


---

Let me know if you'd like:

- 🌐 Multilingual support in the README
- 📸 Screenshots or Telegram bot demo GIF
- 📦 Release packaging guide for Koyeb/Render/VPS

Ready to add badges (build passing, stars, license) or deployment instructions too!
