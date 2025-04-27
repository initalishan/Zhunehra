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
from dotenv import load_dotenv


queue_lock = Lock()

queues = {}  
queue_position = {}  
current_ind = {}
load_dotenv()
MAX_DURATION = int(os.environ["MAX_DURATION"])

async def add_to_queue(song_name, chat_id, mention):
    async with queue_lock:
        status = await zhunehra.send_message(chat_id, "🔎")
        queues.setdefault(chat_id, [])
        queue_position.setdefault(chat_id, 0)
        current_ind.setdefault(chat_id, 0)

        try:
            data = await meta_data(song_name, chat_id)
            title, artist, duration_text, thumbnail = data
            duration = int(duration_text.split(":")[0]) * 60 + int(duration_text.split(":")[1])

            if duration > MAX_DURATION:
                await status.edit(f"**Skipped:** `{title}`\n**Reason:** Song duration exceeds allowed limit.")
                if thumbnail != "db/zhunehra.png" and os.path.exists(thumbnail):
                    os.remove(thumbnail)
                return

            queues[chat_id].append((song_name, mention))

            if len(queues[chat_id]) == 1:
                path = await download(song_name, "m4a", chat_id)
                await Play_Audio(chat_id, path)
                await Call.change_volume_call(chat_id, 200)
                await playing_message(song_name, chat_id, mention)
                if os.path.exists(path):
                    os.remove(path)
            else:
                queue_position[chat_id] += 1
                await queue_message(song_name, chat_id, queue_position[chat_id], mention)

        except Exception as e:
            await zhunehra.send_message(chat_id, f"Error: {str(e)}")
        finally:
            await status.delete()

async def play_next(chat_id):
    async with queue_lock:
        if chat_id not in queues or not queues[chat_id]:
            await Call.leave_call(chat_id)
            await zhunehra.send_message(chat_id, "**Queue finished,** Leaving voice chat.")
            queues.pop(chat_id, None)
            queue_position.pop(chat_id, None)
            current_ind.pop(chat_id, None)
            return

        current_ind[chat_id] += 1
        index = current_ind[chat_id]

        if index >= len(queues[chat_id]):
            await Call.leave_call(chat_id)
            await zhunehra.send_message(chat_id, "**Queue finished,** Leaving voice chat.")
            queues.pop(chat_id, None)
            queue_position.pop(chat_id, None)
            current_ind.pop(chat_id, None)
            return

        try:
            song_name, mention = queues[chat_id][index]
            data = await meta_data(song_name, chat_id)
            title, artist, duration_text, thumbnail = data
            duration = int(duration_text.split(":")[0]) * 60 + int(duration_text.split(":")[1])

            if duration > MAX_DURATION:
                await zhunehra.send_message(chat_id, f"**Skipped:** `{title}`\n**Reason:** Song duration exceeds allowed limit.")
                if thumbnail != "db/zhunehra.png" and os.path.exists(thumbnail):
                    os.remove(thumbnail)
                await play_next(chat_id)
                return

            path = await download(song_name, "m4a", chat_id)
            await Play_Audio(chat_id, path)
            await playing_message(song_name, chat_id, mention)
            if os.path.exists(path):
                os.remove(path)

        except Exception as e:
            await zhunehra.send_message(chat_id, f"Error: {str(e)}")

@Call.on_update(filters.stream_end())
async def stream_end(_, update: Update):
    chat_id = update.chat_id
    if chat_id in queues:
        await play_next(chat_id)

async def playing_message(song_name, chat_id, mention):
    data = await meta_data(song_name, chat_id)
    title, artist, duration_text, thumbnail = data

    await zhunehra.send_file(
        chat_id,
        file=thumbnail,
        caption=f"**{title}**\n\n**Artist:** {artist}\n**Duration:** {duration_text}\n**Requested by:** {mention}",
        buttons=play_buttons
    )

    if thumbnail != "db/zhunehra.png" and os.path.exists(thumbnail):
        os.remove(thumbnail)

async def queue_message(song_name, chat_id, queue_pos, mention):
    data = await meta_data(song_name, chat_id)
    title, artist, duration_text, thumbnail = data

    await zhunehra.send_message(
        chat_id,
        f"**Added to queue:**\n\n**Title:** {title}\n**Artist:** {artist}\n**Duration:** {duration_text}\n**Requested by:** {mention}\n**Queue Position:** #{queue_pos}",
        buttons=queue_buttons
    )

    if thumbnail != "db/zhunehra.png" and os.path.exists(thumbnail):
        os.remove(thumbnail)

async def replay(event):
    user = await event.get_sender()
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    chat_id = event.chat_id

    if chat_id in queues and queues[chat_id]:
        status = await event.reply("**Replaying current track...**")

        index = current_ind.get(chat_id, 0)
        song_name, requested_by = queues[chat_id][index]

        try:
            path = await download(song_name, "m4a", chat_id)
            await Play_Audio(chat_id, path)
            await playing_message(song_name, chat_id, requested_by)
            await status.edit(f"**Replay Started!**\n\n**Requested by:** {mention}")
        except Exception as e:
            await status.edit(f"Replay failed: {str(e)}")
        finally:
            if os.path.exists(path):
                os.remove(path)
    else:
        await event.reply(f"**Nothing is playing to replay,** {mention}.")