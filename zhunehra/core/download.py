from yt_dlp import YoutubeDL


async def is_youtube_url(text):
    return text.startswith("http://") or text.startswith("https://")

async def download(name, format, chat_id):
    path = ""
    if format == "m4a":
        options = {
            "format": "bestaudio[ext=m4a]",
            "outtmpl": f"db/song_{chat_id}.m4a",
        }
        path = f"db/song_{chat_id}.m4a"
    else:
        options = {
            "format": "best",
            "outtmpl": f"db/video_{chat_id}.mp4"
        }
        path = f"db/video_{chat_id}.mp4"
    query = name if await is_youtube_url(name) else f"ytsearch:{name}"
    with YoutubeDL(options) as ydl:
        ydl.download([query])
    return path
        