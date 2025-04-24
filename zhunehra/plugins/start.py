from zhunehra.core.module_injector import *
from zhunehra.utils.start import start_buttons
from os import environ
from dotenv import load_dotenv
from json import load, dump
from telethon.tl.functions.photos import GetUserPhotosRequest
import os

load_dotenv()
chat_log = int(environ["chat_log"])
class start:
    @zhunehra.on(events.NewMessage(pattern=r"\/start"))
    async def start(event):
        sender = await event.get_sender()
        sender_id = event.sender.id
        username = sender.username
        first_name = sender.first_name or ""
        last_name = sender.last_name or ""
        full_name = (first_name + " " + last_name).strip()
        status = await event.respond("👀")
        await zhunehra.send_file(
            event.chat_id,
            file="db/zhunehra.png",
            caption=f"Hey there, [{full_name}](tg://user?id={sender_id}),\n\nWelcome to **[Zhunehra](https://t.me/zhunehra_bot)** your group's personal music DJ.\n\nWith me you can:**\n- Download audio and videos from Youtube using link or name.\n- Play them live in group voice chat.\n- Use powerful commands to control the stream.**\n\nPress the given help button below to get more informention.",
            buttons=start_buttons,
            parse_mode="md"
            )
        await status.delete()
        try:
            with open("db/users.json", "r") as f:
                users = load(f)
        except Exception:
            users = []
        if not sender_id in users:
            users.append(sender_id)
            with open("db/users.json", "w") as f:
                dump(users, f, indent=4)
                photos = await zhunehra(GetUserPhotosRequest(sender_id, offset=0, max_id=0, limit=1))
                if photos.photos:
                    photo = photos.photos[0]
                    file = await zhunehra.download_media(photo, file="db/sender_profile.png")
                await zhunehra.send_file(chat_log, file=file, caption=f"New user started the bot.\n\nUsername: @{username}\nName: {full_name}\nId: {sender_id}", force_document=False)
                os.remove(file)