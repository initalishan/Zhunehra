from zhunehra.core.module_injector import *
from zhunehra.core.play import Play_Audio
from zhunehra.core.download import download
from zhunehra.core.metadata import meta_data
from zhunehra.utils.play import play_buttons
from zhunehra.utils.queue import queue_buttons
from pytgcalls import filters
from pytgcalls.types import Update
import os

queue = []
queue_position = 0
current_index = 1
url_mention = ""

async def add_to_queue(song_name, chat_id, mention):
    global queue_position
    global queue
    global url_mention
    url_mention = mention
    status = await zhunehra.send_message(chat_id, "🔎")
    if len(queue) < 1:
        queue.append(song_name)
        path = await download(queue[queue_position], "m4a", chat_id)
        await Play_Audio(chat_id, path)
        await Call.change_volume_call(chat_id, 200)
        await playing_message(song_name, chat_id)
        os.remove(path)
    else:
        queue_position +=1
        queue.append(song_name)
        await queue_message(song_name, chat_id, queue_position)
    await status.delete()
        
async def play_next(chat_id):
    global queue
    global current_index
    global queue_position
    if current_index < len(queue):
        path = await download(queue[current_index], "m4a", chat_id)
        print(queue)
        print(path)
        await Play_Audio(chat_id, path)
        await playing_message(queue[current_index], chat_id)
        current_index += 1
        os.remove(path)
    else:
        queue.clear()
        current_index = 0
        queue_position = 0
        await Call.leave_call(chat_id)
        await zhunehra.send_message(chat_id, "Queue finished, Leaving voice chat.")
    
@Call.on_update(filters.stream_end())
async def stream_end(_, update: Update):
    chat_id = update.chat_id
    await play_next(chat_id)
        
async def playing_message(song_name, chat_id):
    global url_mention
    data = await meta_data(song_name, chat_id)
    await zhunehra.send_file(
        chat_id,
        file=data[3],
        caption=f"**{data[0]}**\n\n**Artist:** {data[1]}\n**Duration:** {data[2]}\n**Requested by:** {url_mention}",
        buttons=play_buttons
    )
    if data[3] == "db/zhunehra.png":
        pass
    else:
        if os.path.exists(data[3]):
            os.remove(data[3])
async def queue_message(song_name, chat_id, queue_position):
    data = await meta_data(song_name, chat_id)
    await zhunehra.send_message(
        chat_id,
        f"**Added to queue.**\n\n{data[0]}\n\n**Artist:** {data[1]}\n**Duration:** {data[2]}\n**Queue Position:** #{queue_position}",
        buttons=queue_buttons
    )
    if data[3] == "db/zhunehra.png":
        pass
    else:
        os.remove(data[3])