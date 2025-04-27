from yt_dlp import YoutubeDL
from PIL import Image
from os import path, remove


async def is_youtube_url(text):
    return text.startswith("http://") or text.startswith("https://")
    
async def meta_data(song_name, chat_id):
    title = "Unknown Title"
    artist = "Unknown Artist"
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
            query = song_name if await is_youtube_url(song_name) else f"ytsearch:{song_name}"
            result = ydl.extract_info(query, download=True)
            entries = result.get("entries", [])
            if not entries:
                raise Exception("No results found for the query.")
            
            info = entries[0]
            title = info.get("title", "Unknown Title")
            artist = info.get("uploader", "Unknown Artist")
            raw_duration = info.get("duration", 0)
            try:
                raw_duration = int(raw_duration)
            except (ValueError, TypeError):
                raw_duration = 0

        except Exception as e:
            print(f"[Metadata Error] {e}")

    path = f"{thumbnail}.webp"
    final_thumbnail = "db/zhunehra.png"

    try:
        if path.exists(path):
            img = Image.open(path)
            final_thumbnail = path.replace(".webp", ".png")
            img.save(final_thumbnail, "PNG")
        else:
            fallback_jpg = f"db/thumb_{chat_id}.jpg"
            if path.exists(fallback_jpg):
                final_thumbnail = fallback_jpg
    except Exception as e:
        print(f"[Thumbnail Error] {e}")
    try:
        if path.exists(f"db/thumb_{chat_id}.webp"):
            remove(f"db/thumb_{chat_id}.webp")
    except Exception as e:
        print(f"[Cleanup Error] {e}")

    if raw_duration >= 3600:
        hours, remainder = divmod(raw_duration, 3600)
        minutes, secs = divmod(remainder, 60)
        display_duration = f"{hours}:{minutes:02}:{secs:02}"
    else:
        minutes, secs = divmod(raw_duration, 60)
        display_duration = f"{minutes}:{secs:02}"

    data = [title, artist, display_duration, final_thumbnail]
    return data