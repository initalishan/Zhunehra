from zhunehra.core import clients
from zhunehra.utils.db import users_collection, groups_collection
from dotenv import load_dotenv
from telethon import events
from os import environ

zhunehra = clients.zhunehra
load_dotenv()
sudo_users = int(environ["sudo_users"])

@zhunehra.on(events.NewMessage(pattern=r"\/status"))
async def status_handler(event):
    sender = await event.get_sender()
    sender_id = sender.id
    if sender_id == sudo_users:
        total_users = users_collection.count_documents({})
        total_groups = groups_collection.count_documents({})
        await event.reply(f"Total users: {total_users}\nTotal chats: {total_groups}")