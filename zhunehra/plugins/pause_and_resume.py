from zhunehra.core import clients
from telethon import events
from zhunehra.misc.queue import queues

zhunehra = clients.zhunehra
music = clients.music
is_playing = True


@zhunehra.on(events.NewMessage(pattern=r"\/pause"))
async def pause_handler(event):
    if event.is_group or event.is_channel:
        user = await event.get_sender()
        chat = await event.get_chat()
        rights = await zhunehra.get_permissions(chat.id, user.id)
        if not rights.is_admin:
            await event.reply("You must be an admin to use this.")
            return
        try:
            await event.delete()
            await pause(event)
        except Exception:
            pass
    else:
        await event.reply("This command only for groups.")
    
@zhunehra.on(events.CallbackQuery(data=b"pause"))
async def pause_callback(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    rights = await zhunehra.get_permissions(chat.id, user.id)
    if not rights.is_admin:
        await event.answer("You must be an admin to use this.", alert=True)
        return
    await pause(event)
    
async def pause(event):
    global is_playing
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
    user = await event.get_sender()
    if chat_id in queues and len(queues[chat_id]) > 0:
        try:
            mention = f"[{user.first_name}](tg://user?id={user.id})"
        except Exception:
            mention = "Anonymous"
        if is_playing:
            await music.pause(chat_id)
            is_playing = False
            await event.reply(f"**Stream is paused.\nPuased by:** {mention}")
        else:
            await event.reply(f"**Stream is already paused**: {mention}.")
    else:
        await event.reply("Zhunehra is not streaming.")
                          
@zhunehra.on(events.NewMessage(pattern=r"\/resume"))
async def resume_handler(event):
    if event.is_group or event.is_channel:
        user = await event.get_sender()
        chat = await event.get_chat()
        rights = await zhunehra.get_permissions(chat.id, user.id)
        if not rights.is_admin:
            await event.reply("You must be an admin to use this.")
            return
        try:
            await event.delete()
            await resume(event)
        except Exception:
            pass
    else:
        await event.reply("This command only for groups.")
    
@zhunehra.on(events.CallbackQuery(data=b"resume"))
async def resume_callback(event):
    user = await event.get_sender()
    chat = await event.get_chat()
    rights = await zhunehra.get_permissions(chat.id, user.id)
    if not rights.is_admin:
        await event.answer("You must be an admin to use this.", alert=True)
        return
    await resume(event)
    
async def resume(event):
    global is_playing
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
    user = await event.get_sender()
    if chat_id in queues and len(queues[chat_id]) > 0:
        try:
            mention = f"[{user.first_name}](tg://user?id={user.id})"
        except Exception:
            mention =  "Anonymous"
        if not is_playing:
            await music.resume(chat_id)
            is_playing = True
            await event.reply(f"**Stream is Resume.\nResumed by:** {mention}")
        else:
            await event.reply(f"**Stream is already Resumed**: {mention}.")
    else:
        await event.reply("Zhunehra is not streaming.")