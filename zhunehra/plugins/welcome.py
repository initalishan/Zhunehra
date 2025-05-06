from telethon import events, Button
from zhunehra.core import clients
from zhunehra.utils.db import welcome_collection
from zhunehra.core.safedict import SafeDict
from config.strings import welcome_caption, left_caption
from zhunehra.core.profile import create_profile_card
from os import remove
from zhunehra.core.sudo import sudo_users

zhunehra = clients.zhunehra

@zhunehra.on(events.NewMessage(pattern=r"\/welcome\s(.+)"))
async def toggle_welcome(event):
    if not event.is_group:
        return await event.reply("This command only for groups.")
    sender = await event.get_sender()
    chat = await event.get_chat()
    is_admin = await event.client.get_permissions(chat.id, sender.id)
    if not (is_admin.is_admin or sender.id in sudo_users):
        return await event.reply("This command only for admins.")
    cmd = event.pattern_match.group(1)
    chat_id = event.chat_id
    if cmd == "on":
        if welcome_collection.find_one({"chat_id": chat_id}):
            return await event.reply("Welcome system already enabled in this group.")
        welcome_collection.insert_one({"chat_id": chat_id})
        await event.reply("Welcome system **enabled** for this group.")
    elif cmd == "off":
        result = welcome_collection.delete_one({"chat_id": chat_id})
        if result.deleted_count == 0:
            return await event.reply("Welcome system is not active in this group.")
        await event.reply("Welcome system **disabled** for this group.")
    else:
        await event.reply("On or off?")
        
@zhunehra.on(events.ChatAction)
async def welcome_leave_handler(event):
    chat_id = event.chat_id
    if not welcome_collection.find_one({"chat_id": chat_id}):
        return

    user = await event.get_user()
    full_name = user.first_name + (f" {user.last_name}" if user.last_name else "")
    user_id = user.id
    username = user.username or "N/A"
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    group_name = event.chat.title
    safe_data = SafeDict(
             mention=mention,
             full_name=full_name,
             group_name=group_name,
             user_id=user_id,
             username=username
        )
    try:
        photo = await zhunehra.download_profile_photo(user.id)
        profile_card = await create_profile_card(photo, full_name, user_id)
        remove(photo)
    except:
        profile_card = await create_profile_card("config/unknown.png", full_name, user_id)

    if event.user_joined or event.user_added:
        caption = welcome_caption.format_map(safe_data)
        buttons = [Button.url("Add me to your group", f"https://t.me/zhunehra?startgroup=true")] 
    elif event.user_left or event.user_kicked:
        caption = left_caption.format_map(safe_data)
        buttons = [Button.url("See User", f"https://t.me/{username}") if username != "N/A" else Button.inline("No Username", b"no_user")]
    try:
        await zhunehra.send_file(
            chat_id,
            file=profile_card,
            caption=caption,
            parse_mode="md",
            buttons=buttons
        )
    except Exception:
        pass
    try:
        remove(profile_card)
    except Exception:
        pass
