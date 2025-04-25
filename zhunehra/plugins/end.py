from zhunehra.core.module_injector import *
from zhunehra.plugins.queue import queue, current_index, queue_position


@zhunehra.on(events.NewMessage(pattern=r"\/stop"))
async def stop_handler(event):
    await stop_song(event)
    
@zhunehra.on(events.NewMessage(pattern=r"\/end"))
async def end_handler(event):
    await stop_song(event)
        
@zhunehra.on(events.CallbackQuery(data=b"stop"))
async def callback_stop(event):
    await stop_song(event)
        
async def stop_song(event):
    user = await event.get_sender()
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    try:
        await event.delete()
    except Exception:
        pass
    global queue_position, queue, current_index
    if len(queue) > 0:
        chat_id = event.chat_id
        queue.clear()
        queue_position = 0
        current_index = 0
        await Call.leave_call(chat_id)
        await event.reply(f"**Stream ended.\nEnd by:**{mention}")
    else:
        return await event.respond("Zhunehra is not streaming.")