from zhunehra.core import clients
from zhunehra.misc.metadata import meta_data
from zhunehra.misc.download import download
from zhunehra.utils.download import download_buttons
from zhunehra.utils.subscibe import subscribe
import os
from telethon import events
    
    
zhunehra = clients.zhunehra
META_DATA = None
song_name = None
data = []
    
@zhunehra.on(events.NewMessage(pattern=r"\/download(?:\s+(.*))?"))
async def Download(event):
    global META_DATA
    global song_name
    global data
    chat_id = event.chat_id
    song_name = event.pattern_match.group(1)
    if event.is_private: 
        if not song_name:
            await event.reply("Please provide a name or YouTube URL after `/download`.")
            return
        searchmsg = await event.reply(f"Searching for {song_name}")
        data = await meta_data(song_name, "m4a", chat_id)
        await searchmsg.delete()
        META_DATA = await zhunehra.send_file(
            chat_id,
            file=f"{data[4]}",
            caption=f"**{data[1]}**\n\n**Artist:** {data[2]}\n**Duration**: {data[3]}",
            buttons=download_buttons
        )
    else:
        await event.reply("This command works on, only private.")
                
@zhunehra.on(events.CallbackQuery(data=b"audio"))
async def Download_Audio(event):
    global META_DATA
    global song_name
    global data
    chat_id = event.chat_id
    status = await event.respond("Downloading..")
    await META_DATA.delete()
    path = await download(song_name, "m4a", chat_id)
    await status.edit("Uploading..")
    await zhunehra.send_file(chat_id, file=path, thumb=data[4], caption=f"**{data[1]}**\n\n**Artist:** {data[2]}\n**Duration**: {data[3]}", buttons=subscribe, supports_streaming=True)
    await status.delete()
    os.remove(path)
    os.remove(data[4])
            
@zhunehra.on(events.CallbackQuery(data=b"mp4"))
async def Download_Video(event):
    global META_DATA
    global song_name
    global data
    chat_id = event.chat_id
    status = await event.respond("Downloading..")
    await META_DATA.delete()
    path = await download(song_name, "mp4", chat_id)
    await status.edit("Uploading..")
    await zhunehra.send_file(chat_id, file=path, thumb=data[4], caption=f"**{data[1]}**\n\n**Artist:** {data[2]}\n**Duration**: {data[3]}",buttons=subscribe, supports_streaming=True)
    await status.delete()
    os.remove(path)
    os.remove(data[4])