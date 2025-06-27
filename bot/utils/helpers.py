import os
import re
import math
from pymediainfo import MediaInfo

def get_file_size(size_in_bytes):
    """Convert bytes to human-readable file size (e.g., KB, MB, GB)."""
    if size_in_bytes == 0:
        return "0B"
    
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_in_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_in_bytes / p, 2)
    
    # Handle small sizes more cleanly
    if s.is_integer():
        s = int(s)
    return f"{s} {size_name[i]}"

def format_file_size(size_in_bytes):
    """Alias to get_file_size for convenience."""
    return get_file_size(size_in_bytes)

def sanitize_filename(filename):
    """Remove special characters from filenames to prevent errors."""
    # Preserve unicode characters but remove problematic symbols
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def generate_unique_filename(directory, filename):
    """
    Generate a unique filename in the specified directory.
    If filename exists, appends _1, _2, etc.
    """
    # Sanitize filename first
    safe_name = sanitize_filename(filename)
    base, ext = os.path.splitext(safe_name)
    counter = 1
    new_name = safe_name
    
    while os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{base}_{counter}{ext}"
        counter += 1
        
    return new_name

def get_media_info(file_path):
    """
    Extract metadata from a media file (video/audio/subtitle) using pymediainfo.
    Returns a dictionary with stream info.
    """
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    try:
        media_info = MediaInfo.parse(file_path)
    except Exception as e:
        return {"error": f"MediaInfo error: {str(e)}"}
    
    info = {
        "general": {},
        "video": [],
        "audio": [],
        "text": []
    }

    for track in media_info.tracks:
        if track.track_type == "General":
            info["general"] = {
                "format": track.format or "Unknown",
                "duration": track.duration or 0,
                "file_size": track.file_size or 0,
                "frame_rate": track.frame_rate or 0,
            }
        elif track.track_type == "Video":
            info["video"].append({
                "id": track.stream_identifier or len(info["video"]) + 1,
                "type": "video",
                "codec": track.codec_id or track.format or "Unknown",
                "duration": track.duration or 0,
                "resolution": f"{track.width}x{track.height}" if track.width and track.height else "Unknown",
                "bitrate": track.bit_rate or 0,
                "frame_rate": track.frame_rate or 0,
                "language": track.language or "und",
                "title": track.title or "Video Track"
            })
        elif track.track_type == "Audio":
            info["audio"].append({
                "id": track.stream_identifier or len(info["audio"]) + 1,
                "type": "audio",
                "codec": track.codec_id or track.format or "Unknown",
                "language": track.language or "und",
                "title": track.title or "Audio Track",
                "channels": track.channel_s or "Unknown",
                "bitrate": track.bit_rate or 0,
                "sampling_rate": track.sampling_rate or 0
            })
        elif track.track_type == "Text":
            info["text"].append({
                "id": track.stream_identifier or len(info["text"]) + 1,
                "type": "subtitle",
                "codec": track.codec_id or track.format or "Unknown",
                "language": track.language or "und",
                "title": track.title or "Subtitle Track"
            })

    # Add human-readable sizes
    if "file_size" in info["general"]:
        info["general"]["file_size_human"] = get_file_size(info["general"]["file_size"])
    
    return info

def get_file_name(file):
    """Safely get filename from Telegram file object with fallbacks."""
    # Try different attributes to find filename
    if hasattr(file, 'file_name') and file.file_name:
        return file.file_name
    elif hasattr(file, 'filename') and file.filename:
        return file.filename
    elif hasattr(file, 'title') and file.title:
        return f"{file.title}.mp4"
    
    # Fallback to file ID based name
    file_id = getattr(file, 'file_id', 'unknown_file')
    ext = ".mp4" if hasattr(file, 'mime_type') and 'video' in file.mime_type else ".bin"
    return f"{file_id[:8]}{ext}"
