from zhunehra.core.module_injector import *
from zhunehra.core.metadata import meta_data
from zhunehra.core.download import download
from zhunehra.utils.download import download_buttons
from zhunehra.utils.subscibe import subscribe
import os


META_DATA = None
song_name = None
data = []

class Download:
    @zhunehra.on(events.NewMessage(pattern=r"\/download(?:\s+(.*))?"))
    async def download(event):
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
            data = await meta_data(song_name, chat_id)
            await searchmsg.delete()
            META_DATA = await zhunehra.send_file(
                chat_id,
                file=f"{data[3]}",
                caption=f"**{data[0]}**\n\n**Artist:** {data[1]}\n**Duration**: {data[2]}",
                buttons=download_buttons
            )
            os.remove(data[3])
        else:
            await event.reply("This command works on, only private.")
            
    @zhunehra.on(events.CallbackQuery(data=b"audio"))
    async def download_audio(event):
        global META_DATA
        global song_name
        global data
        chat_id = event.chat_id
        status = await event.respond("Downloading..")
        await META_DATA.delete()
        path = await download(song_name, "m4a", chat_id)
        os.rename(path, f"db/{data[0]}.m4a")
        path = f"db/{data[0]}.m4a"
        await status.edit("Uploading..")
        await zhunehra.send_file(chat_id, file=path, caption=f"**{data[0]}**\n\n**Artist:** {data[1]}\n**Duration**: {data[2]}",buttons=subscribe)
        await status.delete()
        os.remove(path)
        
    @zhunehra.on(events.CallbackQuery(data=b"mp4"))
    async def download_audio(event):
        global META_DATA
        global song_name
        global data
        chat_id = event.chat_id
        status = await event.respond("Downloading..")
        await META_DATA.delete()
        path = await download(song_name, "mp4", chat_id)
        os.rename(path, f"db/{data[0]}.mp4")
        path = f"db/{data[0]}.mp4"
        await status.edit("Uploading..")
        await zhunehra.send_file(chat_id, file=path, caption=f"**{data[0]}**\n\n**Artist:** {data[1]}\n**Duration**: {data[2]}",buttons=subscribe)
        await status.delete()
        os.remove(path)