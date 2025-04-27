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

queues = {}
queue_position = {} 
current_ind = {} 
current_playing_index = {}

async def add_to_queue(song_name, chat_id, mention):
    async with queue_lock:
        status = await zhunehra.send_message(chat_id, "🔎")
        
        if chat_id not in queues:
            queues[chat_id] = []
            queue_position[chat_id] = 0
            current_ind[chat_id] = 0
            current_playing_index[chat_id] = 0
        try:
            if len(queues[chat_id]) < 1:
                path = await download(queues[chat_id][0][0], "m4a", chat_id)
                queues[chat_id].append((song_name, mention))
                await Play_Audio(chat_id, path)
                await Call.change_volume_call(chat_id, 200)
                await playing_message(song_name, chat_id, mention)
                os.remove(path)
            else:
                queue_position[chat_id] += 1
                queues[chat_id].append((song_name, mention))
                await queue_message(song_name, chat_id, queue_position[chat_id], mention)
        except Exception as e:
            await zhunehra.send_message(chat_id, str(e))

        await status.delete()

async def play_next(chat_id):
    if chat_id not in queues or not queues[chat_id]:
        await Call.leave_call(chat_id)
        await zhunehra.send_message(chat_id, "Queue finished, Leaving voice chat.")
        queues.pop(chat_id, None)
        queue_position.pop(chat_id, None)
        current_ind.pop(chat_id, None)
        current_playing_index.pop(chat_id, None)
        return
    current_ind[chat_id] = current_ind.get(chat_id, 0) + 1
    if current_ind[chat_id] >= len(queues[chat_id]):
        await Call.leave_call(chat_id)
        await zhunehra.send_message(chat_id, "Queue finished, Leaving voice chat.")
        queues.pop(chat_id, None)
        queue_position.pop(chat_id, None)
        current_ind.pop(chat_id, None)
        current_playing_index.pop(chat_id, None)
        return
    try:
        path = await download(song_name, "m4a", chat_id)
        index = current_ind[chat_id]
        current_playing_index[chat_id] = index
        song_name, mention = queues[chat_id][index]
        await Play_Audio(chat_id, path)
        await playing_message(song_name, chat_id, mention)
    except Exception as e:
        await zhunehra.send_message(chat_id, str(e))
    if os.path.exists(path):
        os.remove(path)


@Call.on_update(filters.stream_end())
async def stream_end(_, update: Update):
    chat_id = update.chat_id
    if chat_id in queues:
        await play_next(chat_id)

async def playing_message(song_name, chat_id, mention):
    data = await meta_data(song_name, chat_id)
    await zhunehra.send_file(
        chat_id,
        file=data[3],
        caption=f"**{data[0]}**\n\n**Artist:** {data[1]}\n**Duration:** {data[2]}\n**Requested by:** {mention}",
        buttons=play_buttons
    )
    if data[3] != "db/zhunehra.png" and os.path.exists(data[3]):
        os.remove(data[3])

async def queue_message(song_name, chat_id, queue_pos, mention):
    data = await meta_data(song_name, chat_id)
    await zhunehra.send_message(
        chat_id,
        f"**Added to queue.**\n\n{data[0]}\n\n**Artist:** {data[1]}\n**Duration:** {data[2]}\n**Requested by:** {mention}\n**Queue Position:** #{queue_pos}",
        buttons=queue_buttons
    )
    if data[3] != "db/zhunehra.png":
        os.remove(data[3])

async def replay(event):
    user = await event.get_sender()
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    chat_id = event.chat_id

    if chat_id in queues and len(queues[chat_id]) > 0:
        status = await event.reply("**Replaying...**")
        index = current_playing_index.get(chat_id, 0)
        song_name, requested_by = queues[chat_id][index]
        path = await download(song_name, "m4a", chat_id)
        await Play_Audio(chat_id, path)
        await playing_message(song_name, chat_id, requested_by)
        await status.edit(f"**Replay Started.\nReplay by:** {mention}")
        os.remove(path)
    else:
        await event.reply(f"**Zhunehra is not streaming: **{mention}")
