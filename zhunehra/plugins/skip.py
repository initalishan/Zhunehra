from zhunehra.core import clients
from telethon import events
from zhunehra.misc.queue import play_next, queues
from asyncio import create_task

zhunehra = clients.zhunehra

@zhunehra.on(events.NewMessage(pattern=r"\/skip"))
async def skip_handler(event):
    if event.is_group or event.is_channel:
        user = await event.get_sender()
        chat = await event.get_chat()
        rights = await zhunehra.get_permissions(chat.id, user.id)
        if not rights.is_admin:
            await event.reply("You must be an admin to use this.")
            return
        try:
            mention = f"[{user.first_name}](tg://user?id={user.id})"
        except Exception:
            mention = "Anonymous"
        chat = await event.get_chat()
        chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
        status = await event.reply("**Skiping..**")
        if chat_id in queues and len(queues[chat_id]) > 0:
            try:
                create_task(play_next(chat_id))
                await event.delete()
            except Exception:
                pass
            await status.edit(f"**Skiped succesfully.\nSkiped by:** {mention}")
        else:
            await event.reply("Zhunehra is not streaming.")
    else:
        await event.reply("This command only for groups.")
    
@zhunehra.on(events.CallbackQuery(data=b"skip"))
async def callback_skip(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    rights = await zhunehra.get_permissions(chat.id, user.id)
    if not rights.is_admin:
        await event.answer("You must be an admin to use this.", alert=True)
        return
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    chat_id = event.chat_id
    status = await event.reply("**Skiping..**")
    if chat_id in queues and len(queues[chat_id]) > 0:
        try:
            create_task(play_next(chat_id))
            await event.delete()
        except Exception:
            pass
        try:
            await status.edit(f"**Skiped succesfully.\nSkiped by:** {mention}")
        except Exception:
            await event.reply(f"**Skiped succesfully.\nSkiped by:** {mention}")
    else:
        await event.reply("Zhunehra is not streaming.")