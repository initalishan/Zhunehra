import re
import os
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

load_dotenv()
MAX_DURATION = os.environ["MAX_DURATION"]

async def is_youtube_url(text):
    return text.startswith("http://") or text.startswith("https://")

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

async def download(name, format, chat_id):
    global MAX_DURATION
    max_duration = int(MAX_DURATION)

    if format == "m4a":
        options = {
            "format": "bestaudio[ext=m4a]",
            "outtmpl": "db/%(title)s.%(ext)s",
            "noplaylist": True,
            "quiet": True
        }
    else:
        options = {
            "format": "best",
            "outtmpl": "db/%(title)s.%(ext)s",
            "noplaylist": True,
            "quiet": True
        }

    song_name = name[0] if isinstance(name, tuple) else name
    query = song_name if await is_youtube_url(song_name) else f"ytsearch:{song_name}"
    
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(query, download=False)
        if "entries" in info:
            info = info["entries"][0]
        
        duration = info.get("duration", 0)
        if duration > max_duration:
            raise Exception(f"Video too long! Max allowed duration is {max_duration//60} minutes.")
        info = ydl.extract_info(query, download=True)
        if "entries" in info:
            info = info["entries"][0]

        downloaded_path = ydl.prepare_filename(info)
        
    return downloaded_path
