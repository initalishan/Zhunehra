from zhunehra.core import clients
from telethon import events
from zhunehra.misc.queue import replay

zhunehra = clients.zhunehra

@zhunehra.on(events.NewMessage(pattern=r"\/replay"))
async def replay_handler(event):
    if event.is_group or event.is_channel:
    	await replay(event)
    else:
        await event.reply("This command works on, Only groups aur channel")
    
@zhunehra.on(events.CallbackQuery(data=b"replay"))
async def replay_callback(event):
    if event.is_group or event.is_channel:
    	await replay(event)
    else:
        await event.reply("This command works on, Only groups aur channel")