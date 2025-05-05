from telethon import events
from zhunehra.core import clients
from zhunehra.utils.db import users_collection, groups_collection
from zhunehra.core.sudo import sudo_users

zhunehra = clients.zhunehra

@zhunehra.on(events.NewMessage(pattern=r"\/broadcast(?:\s+(.+))?"))
async def broadcast_handler(event):
    if event.sender_id not in sudo_users:
        return await event.reply("🚫 **Only Sudo Users can use this command!**")

    reply = await event.get_reply_message()
    message = event.pattern_match.group(1)

    if not message and not reply:
        return await event.reply("**Give me text message after `/broadcast` command or reply to a any message.**")

    status = await event.reply("**Broadcasting to users...**")

    success_users = 0
    for user in users_collection.find():
        try:
            if message:
                await zhunehra.send_message(user["user_id"], message)
            elif reply:
                await reply.forward_to(user["user_id"])
            success_users += 1
        except:
            continue

    await status.edit(f"**Broadcast to users done.**\nNow sending to groups...")

    success_groups = 0
    for group in groups_collection.find():
        try:
            if message:
                await zhunehra.send_message(group["group_id"], message)
            elif reply:
                await reply.forward_to(group["group_id"])
            success_groups += 1
        except:
            continue

    await status.edit(
        f"**Broadcast complete!**\n\n"
        f"Sent to Users: `{success_users}`\n"
        f"Sent to Groups: `{success_groups}`"
    )
