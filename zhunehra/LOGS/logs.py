from zhunehra.utils.db import users_collection, groups_collection
from config.strings import user_log_caption, group_log_caption
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from zhunehra.core import clients
from zhunehra.core.safedict import SafeDict
from dotenv import load_dotenv
from os import environ, remove
from telethon import Button, events

zhunehra = clients.zhunehra
load_dotenv()
chat_log = int(environ["chat_log"])
private_log = 7872695556

async def add_user_db(event):
    user = await event.get_sender()
    user_id = user.id
    if not users_collection.find_one({"user_id": user_id}):
        username = user.username or "Anonymous"
        first_name = user.first_name or ""
        last_name = user.last_name or ""
        full_name = (first_name + " " + last_name).strip()
        safe_data = SafeDict(
            username=username,
            first_name=first_name,
            last_name=last_name,
            full_name=full_name,
            sender_id=user_id,
        )
        users_collection.insert_one({"user_id": user_id})
        photos = await zhunehra(GetUserPhotosRequest(user_id, offset=0, max_id=0, limit=1))
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
        
async def add_group_db(event):
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
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
    
@zhunehra.on(events.NewMessage)
async def logs(event):
    if event.is_private:
        user = await event.get_sender()
        user_id = user.id
        username = user.username or "Anonymous"
        first_name = user.first_name or ""
        last_name = user.last_name or ""
        full_name = (first_name + " " + last_name).strip()
        await add_user_db(event)
        try:
            message = event.message.message
        except:
            message = "User send a file."
        if username != "Anonymous":
            mention = f"[{full_name}](https://t.me/{username})"
        else:
            mention = f"[{full_name}](tg://user?id={user_id})"
        await zhunehra.send_message(private_log, f"Catch New Message!\nSender: {mention}\nSender_id: {user_id}\nMessage: {message}")
    else:
        await add_group_db(event)