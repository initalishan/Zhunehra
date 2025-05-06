import re
from yt_dlp import YoutubeDL

cookie = "cookies/cookies.txt"

async def is_youtube_url(text):
    return text.startswith("http://") or text.startswith("https://")

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

async def download(name, format, chat_id):
    if format == "m4a":
        options = {
            "format": "bestaudio[ext=m4a]",
            "cookiefile": cookie,
            "outtmpl": "config/%(title)s.%(ext)s",
            "noplaylist": True,
            "quiet": True
        }
    else:
        options = {
            "format": "best",
            "cookiefile": cookie,
            "outtmpl": "config/%(title)s.%(ext)s",
            "noplaylist": True,
            "quiet": True
        }

    song_name = name[0] if isinstance(name, tuple) else name
    query = song_name if await is_youtube_url(song_name) else f"ytsearch:{song_name}"
    
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(query, download=False)
        if "entries" in info:
            info = info["entries"][0]
        info = ydl.extract_info(query, download=True)
        if "entries" in info:
            info = info["entries"][0]
        downloaded_path = ydl.prepare_filename(info)
        
    return downloaded_path