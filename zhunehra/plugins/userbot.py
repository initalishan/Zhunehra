from zhunehra.core import clients
from zhunehra.misc.queue import queues, current_ind, queue_position
from pytgcalls import filters
from pytgcalls.types import ChatUpdate, Update
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon import events
import asyncio

assistant = clients.assistant
pending_check = set()
zhunehra = clients.zhunehra
music = clients.music

@music.on_update(filters.chat_update(ChatUpdate.Status.LEFT_CALL))
async def on_call_ended(_, update: Update):
    chat = update.chat_id
    chat_id = int(f"-100{chat}" if not str(chat).startswith("-100") else chat)
    if chat_id in queues and len(queues[chat_id]) > 0:
        queues.pop(chat_id, None)
        current_ind.pop(chat_id, None)
        queue_position.pop(chat_id, None)
        try:
            await zhunehra.send_message(chat_id, "Voice chat ended. Queue cleared.")
        except Exception:
            pass

@assistant.on(events.ChatAction)
async def on_zhunhera_banned(event):
    chat = event.chat_id
    chat_id = int(f"-100{chat}" if not str(chat).startswith("-100") else chat)
    user = await event.get_user()
    if event.user_left or event.user_kicked:
        if user.username == "zhunehra_bot":
            try:
                await assistant(LeaveChannelRequest(chat_id))
                await music.leave_call(chat_id)
                if chat_id in queues and len(queues[chat_id]) > 0:
                    queues.pop(chat_id, None)
                    current_ind.pop(chat_id, None)
                    queue_position.pop(chat_id, None)
            except: 
                pass
    if chat_id in queues:
        return
    if chat_id in pending_check:
        return
    pending_check.add(chat_id)
    await asyncio.sleep(1800) 
    if chat_id not in queues:
        try:
            await assistant(LeaveChannelRequest(chat_id))
        except:
            pass
    pending_check.discard(chat_id)