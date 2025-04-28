from zhunehra.core.module_injector import *
from zhunehra.plugins.queue import play_next

@zhunehra.on(events.NewMessage(pattern=r"\/skip"))
async def skip_handler(event):
    if event.is_group:
        user = await event.get_sender()
        try:
            mention = f"[{user.first_name}](tg://user?id={user.id})"
        except Exception:
            mention = "Anonymous"
        chat = await event.get_chat()
        chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
        status = await event.reply("**Skiping..**")
        try:
            await play_next(chat_id)
            await event.delete()
        except Exception:
            pass
        await status.edit(f"**Skiped succesfully.\nSkiped by:** {mention}")
    else:
        await event.reply("This command only for groups.")
    
@zhunehra.on(events.CallbackQuery(data=b"skip"))
async def callback_skip(event):
    user = await event.get_sender()
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    chat_id = event.chat_id
    status = await event.reply("**Skiping..**")
    try:
        await play_next(chat_id)
        await event.delete()
    except Exception:
        pass
    await status.edit(f"**Skiped succesfully.\nSkiped by:** {mention}")