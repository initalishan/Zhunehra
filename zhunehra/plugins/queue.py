from zhunehra.core.module_injector import *
from zhunehra.core.play import Play_Audio
from zhunehra.core.download import download
from zhunehra.core.metadata import meta_data
from pytgcalls import filters
from pytgcalls.types import Update
import os

queue = []
queue_position = 0
paths = []
paths_index = 0

async def add_to_queue(song_name, chat_id, mention):
    global queue_position
    global queue
    if len(queue) == queue_position:
        queue.append(song_name)
        path = await download(queue[queue_position], "m4a", chat_id)
        await Play_Audio(chat_id, path)
        data = await meta_data(song_name, chat_id)
        await zhunehra.send_file(
                chat_id,
                file=data[3],
                caption=f"**{data[0]}**\n\n**Artist:** {data[1]}\n**Duration:** {data[2]}\n**Requested by:** {mention}"
            )
    else:
        data = await meta_data(song_name, chat_id)
        queue_position += 1
        queue.append(song_name)
        await zhunehra.send_message(
            chat_id,
            f"**Added to queue.**\n\n{data[0]}\n\n**Artist:** {data[1]}\n**Duration:** {data[2]}\n**Queue Position:** #{queue_position}"
        )
        if (len(queue) -1) == queue_position:
            path = await download(queue[queue_position], "m4a", chat_id)
            paths.append(path)
        
async def play_next(chat_id):
    global queue
    global queue_position
    if len(queue) > queue_position and len(queue) < (1+queue_position):
        await Play_Audio(chat_id, queue[queue_position])
   
@Call.on_update(filters.stream_end())
async def stream_end(_, update: Update):
    global paths_index
    global paths
    global queue
    global queue_position
    chat_id = update.chat_id
    path = paths[paths_index]
    print(f"Now playing {path}")
    await Play_Audio(chat_id, path)
    if paths_index > (len(paths)):
        paths_index += 1