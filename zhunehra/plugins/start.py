from asyncio import sleep
from zhunehra.core import clients
from zhunehra.utils.start import *
from zhunehra.core.safedict import SafeDict
from telethon import events
from config.strings import start_caption, start_group_caption

zhunehra = clients.zhunehra

async def animated_loading(event, text="Starting Zhunehra"):
    dots = ["", ".", "..", "..."]
    msg = await event.respond(f"{text}")
    prev = ""
    for i in range(8):
        await sleep(0.3)
        current = f"{text}{dots[i % 4]}"
        if current != prev:
            try:
                await msg.edit(current)
                prev = current
            except Exception:
                pass
    return msg

@zhunehra.on(events.NewMessage(pattern=r"\/start"))
async def Start(event):
    global user_log_caption
    global group_log_caption
    try:
        await event.delete()
    except Exception:
        pass
    global start_caption
    status = await animated_loading(event, "Starting Zhunehra")
    if event.is_private:
        sender = await event.get_sender()
        sender_id = event.sender.id or "Anonymous"
        username = sender.username or "Anonymous"
        first_name = sender.first_name or ""
        last_name = sender.last_name or ""
        full_name = (first_name + " " + last_name).strip()
        safe_data = SafeDict(
            username=username,
            first_name=first_name,
            last_name=last_name,
            full_name=full_name,
            sender_id=sender_id,
        )
        formated_start_caption = start_caption.format_map(safe_data)
        await zhunehra.send_file(
            event.chat_id,
            file="config/zhunehra.png",
            caption=formated_start_caption,
            buttons=start_buttons,
            parse_mode="md"
            )
        try:
            await status.delete()
        except Exception:
            pass
    else:
        await event.reply(
            start_group_caption,
            buttons=start_group_buttons
        )
        try:
            await status.delete()
        except Exception:
            pass