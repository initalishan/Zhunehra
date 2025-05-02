from zhunehra.core import clients
from telethon import events
from zhunehra.misc.queue import queues, current_ind, queue_position

zhunehra = clients.zhunehra
music = clients.music
@zhunehra.on(events.NewMessage(pattern=r"\/stop"))
async def Stop(event):
    if event.is_group or event.is_channel:
        try:
            await stop_song(event)
        except Exception:
            pass
    else:
        await event.reply("This command only for groups.")

@zhunehra.on(events.NewMessage(pattern=r"\/end"))
async def End(event):
    if event.is_group or event.is_channel:
        try:
            await stop_song(event)
        except Exception:
            pass
    else:
        await event.reply("This command only for groups.")

@zhunehra.on(events.CallbackQuery(data=b"stop"))
async def Stop_Callback(event):
    try:
        await stop_song(event)
    except Exception:
        pass

async def stop_song(event):
    user = await event.get_sender()
    try:
        mention = f"[{user.first_name}](tg://user?id={user.id})"
    except Exception:
        mention = "Anonymous"
    try:
        await event.delete()
    except Exception:
        pass
    
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
    if chat_id in queues and len(queues[chat_id]) > 0:
        queues.pop(chat_id, None)
        queue_position.pop(chat_id, None)
        current_ind.pop(chat_id, None)
        await music.leave_call(chat_id)
        await event.reply(f"**Stream ended.\nEnd by:** {mention}")
    else:
        await event.respond("Zhunehra is not streaming.")
