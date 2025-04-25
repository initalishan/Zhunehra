from zhunehra.core.module_injector import *

is_playing = True


@zhunehra.on(events.NewMessage(pattern=r"\/pause"))
async def pause_handler(event):
    await event.delete()
    await pause(event)
    
@zhunehra.on(events.CallbackQuery(data=b"pause"))
async def resume_callback(event):
    await pause(event)
    
async def pause(event):
    global is_playing
    chat_id = event.chat_id
    user = await event.get_sender()
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    if is_playing:
        await Call.pause(chat_id)
        is_playing = False
        await event.respond(f"**Stream is paused.\nPuased by:** {mention}")
    else:
        await event.respond(f"**Stream is already paused**: {mention}.")
        
zhunehra.on(events.NewMessage(pattern=r"\/resume"))
async def resume_handler(event):
    await event.delete()
    await resume(event)
    
@zhunehra.on(events.CallbackQuery(data=b"resume"))
async def resume_callback(event):
    await resume(event)
    
async def resume(event):
    global is_playing
    chat_id = event.chat_id
    user = await event.get_sender()
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    if not is_playing:
        await Call.resume(chat_id)
        is_playing = True
        await event.respond(f"**Stream is Resume.\nResumed by:** {mention}")
    else:
        await event.respond(f"**Stream is already Resumed**: {mention}.")