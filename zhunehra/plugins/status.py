from zhunehra.core import clients
from zhunehra.utils.db import users_collection, groups_collection
from telethon import events
from zhunehra.core.sudo import sudo_users
from zhunehra.core.ping import get_ping
from zhunehra.core.uptime import get_uptime
from zhunehra.misc.queue import queues

zhunehra = clients.zhunehra

@zhunehra.on(events.NewMessage(pattern=r"\/status"))
async def status_handler(event):
    sender = await event.get_sender()
    sender_id = sender.id
    await event.delete()
    if sender_id in sudo_users:
        ping = get_ping()
        uptime = get_uptime()
        total_users = users_collection.count_documents({})
        total_groups = groups_collection.count_documents({})
        await zhunehra.send_file(
            event.chat_id,
            file="config/zhunehra.png",
            caption=f"**Zhunehra's status.**\n\n**Ping:** {ping}\n**Uptime:** {uptime}\n**Playing on:** {len(queues)} Voice chats\n\n**Total users:** {total_users}\n**Total chats:** {total_groups}"
            )
    else:
        await event.reply("Beta pahle @initalishan ke pass jao aur sudo lo.")