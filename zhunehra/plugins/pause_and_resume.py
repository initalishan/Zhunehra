from zhunehra.core.module_injector import *

is_playing = True


@zhunehra.on(events.NewMessage(pattern=r"\/pause"))
async def pause_handler(event):
    if event.is_group:
        try:
            await event.delete()
            await pause(event)
        except Exception:
            pass
    else:
        await event.reply("This command only for groups.")
    
@zhunehra.on(events.CallbackQuery(data=b"pause"))
async def pause_callback(event):
    await pause(event)
    
async def pause(event):
    global is_playing
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
    user = await event.get_sender()
    try:
        mention = f"[{user.first_name}](tg://user?id={user.id})"
    except Exception:
        mention = "Anonymous"
    if is_playing:
        await Call.pause(chat_id)
        is_playing = False
        await event.respond(f"**Stream is paused.\nPuased by:** {mention}")
    else:
        await event.respond(f"**Stream is already paused**: {mention}.")
        
@zhunehra.on(events.NewMessage(pattern=r"\/resume"))
async def resume_handler(event):
    if event.is_group:
        try:
            await event.delete()
            await resume(event)
        except Exception:
            pass
    else:
        await event.reply("This command only for groups.")
    
@zhunehra.on(events.CallbackQuery(data=b"resume"))
async def resume_callback(event):
    await resume(event)
    
async def resume(event):
    global is_playing
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
    user = await event.get_sender()
    try:
        mention = f"[{user.first_name}](tg://user?id={user.id})"
    except Exception:
        mention =  "Anonymous"
    if not is_playing:
        await Call.resume(chat_id)
        is_playing = True
        await event.respond(f"**Stream is Resume.\nResumed by:** {mention}")
    else:
        await event.respond(f"**Stream is already Resumed**: {mention}.")