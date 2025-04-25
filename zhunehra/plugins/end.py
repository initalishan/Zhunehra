from zhunehra.core.module_injector import *
from zhunehra.plugins.queue import queue, current_index, queue_position


@zhunehra.on(events.NewMessage(pattern=r"\/stop"))
async def stop(event):
    await stop_song(event)
    
@zhunehra.on(events.NewMessage(pattern=r"\/end"))
async def stop(event):
    await stop_song(event)
        
async def stop_song(event):
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
        await event.reply("stream ended.")
    else:
        return await event.respond("Zhunehra is not streaming.")