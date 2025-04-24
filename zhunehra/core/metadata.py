from yt_dlp import YoutubeDL
from PIL import Image
import os

async def meta_data(song_name, chat_id):
    title = ""
    artist = ""
    duration = ""
    thumbnail = f"db/thumb_{chat_id}"
    options = {
        "quiet": True,
        "skip_download": True,
        "writethumbnail": True,
        "outtmpl": thumbnail
    }
    with YoutubeDL(options) as ydl:
        try:
            result = ydl.extract_info(f"ytsearch:{song_name}", download=True)
            info = result["entries"][0]
            title = info.get("title")
            artist = info.get("uploader")
            duration = info.get("duration")
        except Exception as e:
            print(f"Error: {e}")
        path = f"{thumbnail}.webp"
        img = Image.open(path)
        thumbnail = path.replace(".webp", ".png")
        img.save(thumbnail, "PNG")
        minutes, secs = divmod(duration, 60)
        duration = f"{minutes}:{secs:02}"
        os.remove(f"db/thumb_{chat_id}.webp")
    data = [title, artist, duration, thumbnail]
    return data