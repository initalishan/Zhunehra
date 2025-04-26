from zhunehra.core.module_injector import *
from zhunehra.core.play import Play_Audio
from zhunehra.core.download import download
from zhunehra.core.metadata import meta_data
from zhunehra.utils.play import play_buttons
from zhunehra.utils.queue import queue_buttons
from pytgcalls import filters
from pytgcalls.types import Update
import os
from asyncio import Lock

queue_lock = Lock()
queue = []
queue_position = 0
current_index = 1
current_playing_index = 0
active_chat_id = None

async def add_to_queue(song_name, chat_id, mention):
    global queue_position
    global queue
    global active_chat_id
    async with queue_lock:
        status = await zhunehra.send_message(chat_id, "🔎")
        if len(queue) < 1:
            queue.append((song_name, mention))
            path = await download(queue[0][0], "m4a", chat_id)
            await Play_Audio(chat_id, path)
            await Call.change_volume_call(chat_id, 200)
            active_chat_id = chat_id
            await playing_message(song_name, chat_id, mention)
            os.remove(path)
        else:
            queue_position += 1
            queue.append((song_name, mention))
            await queue_message(song_name, chat_id, queue_position, mention)
        await status.delete()
        
async def play_next(chat_id):
    global queue
    global current_index
    global queue_position
    global current_playing_index
    global active_chat_id
    if current_index < len(queue):
        path = await download(queue[current_index][0], "m4a", chat_id)
        await Play_Audio(chat_id, path)
        current_playing_index = current_index
        await playing_message(queue[current_index][0], chat_id, queue[current_index][1])
        current_index += 1
        os.remove(path)
    else:
        queue.clear()
        current_index = 0
        queue_position = 0
        active_chat_id = None
        await Call.leave_call(chat_id)
        await zhunehra.send_message(chat_id, "Queue finished, Leaving voice chat.")
    
@Call.on_update(filters.stream_end())
async def stream_end(_, update: Update):
    chat_id = update.chat_id
    if active_chat_id == chat_id:
        await play_next(chat_id)
        
async def playing_message(song_name, chat_id, mention):
    data = await meta_data(song_name, chat_id)
    await zhunehra.send_file(
        chat_id,
        file=data[3],
        caption=f"**{data[0]}**\n\n**Artist:** {data[1]}\n**Duration:** {data[2]}\n**Requested by:** {mention}",
        buttons=play_buttons
    )
    if data[3] == "db/zhunehra.png":
        pass
    else:
        if os.path.exists(data[3]):
            os.remove(data[3])

async def queue_message(song_name, chat_id, queue_position, mention):
    data = await meta_data(song_name, chat_id)
    await zhunehra.send_message(
        chat_id,
        f"**Added to queue.**\n\n{data[0]}\n\n**Artist:** {data[1]}\n**Duration:** {data[2]}\n**Requested by: **{mention}\n**Queue Position:** #{queue_position}",
        buttons=queue_buttons
    )
    if data[3] == "db/zhunehra.png":
        pass
    else:
        os.remove(data[3])
        
async def replay(event):
    global current_index
    global current_playing_index
    global active_chat_id
    user = await event.get_sender()
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    if len(queue) > 0:
        status = await event.reply("**Replaying...**")
        chat_id = event.chat_id
        if active_chat_id != chat_id:
            await status.edit("**Currently no stream in this chat.**")
            return
        path = await download(queue[current_playing_index][0], "m4a", chat_id)
        await Play_Audio(chat_id, path)
        await playing_message(queue[current_playing_index][0], chat_id, mention)
        await status.edit(f"**Replay Started.\nReplay by:** {mention}")
        os.remove(path)
    else:
        await event.reply(f"**Zhunehra is not streaming: **{mention}")