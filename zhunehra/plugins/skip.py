from zhunehra.core.module_injector import *
from zhunehra.plugins.queue import play_next

@zhunehra.on(events.NewMessage(pattern=r"\/skip"))
async def skip_handler(event):
    user = await event.get_sender()
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    chat_id = event.chat_id
    status = await event.reply("**Skiping..**")
    await play_next(chat_id)
    await event.delete()
    await status.edit(f"**Skiped succesfully.\nSkiped by:** {mention}")
    
@zhunehra.on(events.CallbackQuery(data=b"skip"))
async def callback_skip(event):
    user = await event.get_sender()
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    chat_id = event.chat_id
    status = await event.reply("**Skiping..**")
    await play_next(chat_id)
    await event.delete()
    await status.edit(f"**Skiped succesfully.\nSkiped by:** {mention}")