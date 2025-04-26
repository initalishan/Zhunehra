from zhunehra.core.module_injector import *
from zhunehra.plugins.queue import queue, current_index, queue_position, active_chat_id
from telethon.tl.types import UpdateGroupCall

@zhunehra.on(events.Raw)
async def voice_chat_updates(event):
    global active_chat_id
    if isinstance(event, UpdateGroupCall):
        if event.call and event.call.ended:
            if active_chat_id:
                queue.clear()
                current_index = 0
                queue_position = 0
                await Call.leave_call(active_chat_id)
                await zhunehra.send_message(active_chat_id, "Voice chat has ended.")
                active_chat_id = None
        else:
            if active_chat_id:
                await zhunehra.send_message(active_chat_id, "Voice chat has started or updated.")