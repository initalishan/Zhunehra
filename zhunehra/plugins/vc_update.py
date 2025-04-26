from zhunehra.core.module_injector import *
from zhunehra.plugins.queue import queue, current_index, queue_position
from pytgcalls import filters
from pytgcalls.types import ChatUpdate, Update


@Call.on_update(filters.chat_update(ChatUpdate.Status.LEFT_CALL))
async def on_call_ended(_, update: Update):
    chat_id = update.chat_id
    if len(queue) > 0:
        queue.clear()
        current_index = 0
        queue_position = 0
        await zhunehra.send_message(chat_id, "Voice chat ended. Queue clear.")
    await zhunehra.send_message(chat_id, "Voice chat ended.")