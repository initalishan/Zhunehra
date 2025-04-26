from zhunehra.core.module_injector import *
from zhunehra.plugins.queue import replay

@zhunehra.on(events.NewMessage(pattern=r"\/replay"))
async def replay_handler(event):
    await replay(event)
    
@zhunehra.on(events.CallbackQuery(data=b"replay"))
async def replay_callback(event):
    await replay(event)