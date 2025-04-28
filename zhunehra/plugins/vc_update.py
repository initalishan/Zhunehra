from zhunehra.core.module_injector import *
from zhunehra.plugins.queue import queues, current_ind, queue_position
from pytgcalls import filters
from pytgcalls.types import ChatUpdate, Update

@Call.on_update(filters.chat_update(ChatUpdate.Status.LEFT_CALL))
async def on_call_ended(_, update: Update):
    chat = update.chat_id
    chat_id = int(f"-100{chat}" if not str(chat).startswith("-100") else chat)
    if chat_id in queues and len(queues[chat_id]) > 0:
        queues.pop(chat_id, None)
        current_ind.pop(chat_id, None)
        queue_position.pop(chat_id, None)
        await zhunehra.send_message(chat_id, "Voice chat ended. Queue cleared.")