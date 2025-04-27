from zhunehra.core.module_injector import *
from zhunehra.plugins.queue import queues, current_ind, queue_position

@zhunehra.on(events.NewMessage(pattern=r"\/stop"))
async def stop_handler(event):
    if event.is_group:
        try:
            await stop_song(event)
        except Exception:
            pass
    else:
        await event.reply("This command only for groups.")

@zhunehra.on(events.NewMessage(pattern=r"\/end"))
async def end_handler(event):
    if event.is_group:
        try:
            await stop_song(event)
        except Exception:
            pass
    else:
        await event.reply("This command only for groups.")

@zhunehra.on(events.CallbackQuery(data=b"stop"))
async def callback_stop(event):
    try:
        await stop_song(event)
    except Exception:
        pass

async def stop_song(event):
    user = await event.get_sender()
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    try:
        await event.delete()
    except Exception:
        pass
    
    chat_id = event.chat_id
    if chat_id in queues and len(queues[chat_id]) > 0:
        queues.pop(chat_id, None)
        queue_position.pop(chat_id, None)
        current_ind.pop(chat_id, None)
        await Call.leave_call(chat_id)
        await event.reply(f"**Stream ended.\nEnd by:** {mention}")
    else:
        await event.respond("Zhunehra is not streaming.")
