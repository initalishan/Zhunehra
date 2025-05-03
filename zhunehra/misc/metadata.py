from yt_dlp import YoutubeDL
from zhunehra.core.thumbnail import Thumbnail
import requests
import os

cookie = "cookies/cookies.txt"

async def is_youtube_url(text):
    return text.startswith("http://") or text.startswith("https://")

async def meta_data(song_name, format, chat_id):
    title = "Unknown Title"
    artist = "Unknown Artist"
    url = "url"
    raw_duration = 0
    display_duration = "0:00"
    thumbnail_path = f"config/thumb_{chat_id}.png"

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best" if format == "m4a" else "best",
        "quiet": True,
        "cookiefile": cookie,
        "skip_download": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            query = song_name if await is_youtube_url(song_name) else f"ytsearch:{song_name}"
            result = ydl.extract_info(query, download=False)

            if 'entries' in result:
                info = result['entries'][0]
            else:
                info = result

            url = info.get("url")
            title = info.get("title", "Unknown Title")
            artist = info.get("uploader", "Unknown Artist")
            raw_duration = int(info.get("duration", 0))
            thumbnail_url = info.get("thumbnail")
            
            if raw_duration >= 3600:
                hours, remainder = divmod(raw_duration, 3600)
                minutes, secs = divmod(remainder, 60)
                display_duration = f"{hours}:{minutes:02}:{secs:02}"
            else:
                minutes, secs = divmod(raw_duration, 60)
                display_duration = f"{minutes}:{secs:02}"
                
            if thumbnail_url:
                try:
                    response = requests.get(thumbnail_url, stream=True)
                    if response.status_code == 200:
                        with open(thumbnail_path, "wb") as f:
                            for chunk in response.iter_content(1024):
                                f.write(chunk)
                        thumbnail_path = await Thumbnail(thumbnail_path, title, artist, display_duration)
                    else:
                        thumbnail_path = "config/zhunehra.png"
                except Exception as e:
                    print(f"[Thumbnail Download Error] {e}")
                    thumbnail_path = "config/zhunehra.png"
            else:
                thumbnail_path = "config/zhunehra.png"

        except Exception as e:
            print(f"[Metadata Error] {e}")
            thumbnail_path = "config/zhunehra.png"

    return [url, title, artist, display_duration, thumbnail_path]
