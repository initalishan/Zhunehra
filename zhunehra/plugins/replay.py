from zhunehra.core import clients
from telethon import events
from zhunehra.misc.queue import replay
from asyncio import create_task

zhunehra = clients.zhunehra

@zhunehra.on(events.NewMessage(pattern=r"\/replay"))
async def replay_handler(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    rights = await zhunehra.get_permissions(chat.id, user.id)
    if not rights.is_admin:
        await event.reply("You must be an admin to use this.")
        return
    if event.is_group or event.is_channel:
    	create_task(replay(event))
    else:
        await event.reply("This command works on, Only groups aur channel")
    
@zhunehra.on(events.CallbackQuery(data=b"replay"))
async def replay_callback(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    rights = await zhunehra.get_permissions(chat.id, user.id)
    if not rights.is_admin:
        await event.answer("You must be an admin to use this.", alert=True)
        return
    if event.is_group or event.is_channel:
    	create_task(replay(event))
    else:
        await event.reply("This command works on, Only groups aur channel")