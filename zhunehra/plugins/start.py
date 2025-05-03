from zhunehra.core import clients
from zhunehra.utils.db import users_collection, groups_collection
from zhunehra.utils.start import *
from zhunehra.core.safedict import SafeDict
from os import environ, remove
from telethon import Button, events
from dotenv import load_dotenv
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from config.strings import start_caption, start_group_caption, user_log_caption, group_log_caption

zhunehra = clients.zhunehra
load_dotenv()
chat_log = int(environ["chat_log"])
    
@zhunehra.on(events.NewMessage(pattern=r"\/start"))
async def Start(event):
    global user_log_caption
    global group_log_caption
    try:
        await event.delete()
    except Exception:
        pass
    global start_caption
    status = await event.respond("👀")
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
        if not users_collection.find_one({"user_id": sender_id}):
            users_collection.insert_one({"user_id": sender_id})
            photos = await zhunehra(GetUserPhotosRequest(sender_id, offset=0, max_id=0, limit=1))
            if photos.photos:
                photo = photos.photos[0]
                file = await zhunehra.download_media(photo, file="db/sender_profile.png")
                formated_user_log_caption = user_log_caption.format_map(safe_data)
            else:
                file = "config/zhunehra.png"
            await zhunehra.send_file(
                chat_log,
                file=file,
                caption=formated_user_log_caption,
                force_document=False
                    )
            remove(file)
    else:
        chat = await event.get_chat()
        chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
        await event.reply(
            start_group_caption,
            buttons=start_group_buttons
        )
        try:
            await status.delete()
        except Exception:
            pass
        if not groups_collection.find_one({"group_id": chat_id}):
            groups_collection.insert_one({"group_id": chat_id})
            full_chat = await zhunehra(GetFullChannelRequest(channel=chat_id))
            chat = full_chat.full_chat
            photo = chat.chat_photo
            full_name = chat.about or "No title found"
            username = chat.username if hasattr(chat, "username") and chat.username else None
            safe_data = SafeDict(
                full_name=full_name,
                username=username,
                chat_id=chat_id
            )
            formated_group_log_caption = group_log_caption.format_map(safe_data)
            if photo:
                file = await zhunehra.download_media(photo, file="db/group.png")
            else:
                file = "config/zhunehra.png"
            try:
                result = await zhunehra(ExportChatInviteRequest(chat_id))
                invite_link = result.link
                invite_button = [
                    [Button.url("See Group", invite_link)]
                ]
            except Exception:
                invite_button = [
                    [Button.inline("See Group", data=b"invite_failed")]
                ]
            await zhunehra.send_file(
                chat_log,
                file=file,
                caption=formated_group_log_caption,
                buttons=invite_button,
                force_document=False
                )
            if file != "config/zhunehra.png":
                remove(file)
@zhunehra.on(events.CallbackQuery(data=b"invite_failed"))
async def invite_failed_callback(event):
    await event.answer("Failed to create invite link because zhunehra is not admin and group is private.")