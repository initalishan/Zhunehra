from yt_dlp import YoutubeDL
from PIL import Image
import os

async def meta_data(song_name, chat_id):
    title = ""
    artist = ""
    raw_duration = 0
    display_duration = "0:00"
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
            title = info.get("title", "Unknown Title")
            artist = info.get("uploader", "Unknown Artist")
            raw_duration = info.get("duration", 0)

            try:
                raw_duration = int(raw_duration)
            except (ValueError, TypeError):
                raw_duration = 0

        except Exception as e:
            print("Error in YDL:", e)

    path = f"{thumbnail}.webp"
    if os.path.exists(path):
        img = Image.open(path)
        thumbnail = path.replace(".webp", ".png")
        img.save(thumbnail, "PNG")
    else:
        thumbnail = f"db/thumb_{chat_id}.jpg"
        if not os.path.exists(thumbnail):
            thumbnail = "db/zhunehra.png"

    minutes, secs = divmod(raw_duration, 60)
    display_duration = f"{minutes}:{secs:02}"

    if os.path.exists(f"db/thumb_{chat_id}.webp"):
        os.remove(f"db/thumb_{chat_id}.webp")

    data = [title, artist, display_duration, thumbnail]
    return data
