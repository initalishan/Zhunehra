from yt_dlp import YoutubeDL
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
    thumbnail_path = f"db/thumb_{chat_id}.png"
    if format == "m4a":
        options = {
            "format": "bestaudio[ext=m4a]/bestaudio/best",
            "quiet": True,
            "cookiefile": cookie,
            "skip_download": True,
            "writethumbnail": True,
            "outtmpl": thumbnail_path
        }
    else:
        options = {
            "format": "best",
            "quiet": True,
            "cookiefile": cookie,
            "skip_download": True,
            "writethumbnail": True,
            "outtmpl": thumbnail_path
        }

    with YoutubeDL(options) as ydl:
        try:
            query = song_name if await is_youtube_url(song_name) else f"ytsearch:{song_name}"
            result = ydl.extract_info(query, download=True)
            if 'entries' in result:
                info = result['entries'][0]
            else:
                info = result
            url = info.get("url")
            title = info.get("title", "Unknown Title")
            artist = info.get("uploader", "Unknown Artist")
            raw_duration = info.get("duration", 0)
            try:
                raw_duration = int(raw_duration)
            except (ValueError, TypeError):
                raw_duration = 0

        except Exception as e:
            print(f"[Metadata Error] {e}")

    if not os.path.exists(thumbnail_path):
        thumbnail_path = "db/zhunehra.png"

    if raw_duration >= 3600:
        hours, remainder = divmod(raw_duration, 3600)
        minutes, secs = divmod(remainder, 60)
        display_duration = f"{hours}:{minutes:02}:{secs:02}"
    else:
        minutes, secs = divmod(raw_duration, 60)
        display_duration = f"{minutes}:{secs:02}"

    data = [url, title, artist, display_duration, thumbnail_path]
    return data