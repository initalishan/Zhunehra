import random
import asyncio
from telethon import events, Button
from zhunehra.core import clients
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantsSearch
from config.strings import tag_lines
from zhunehra.core.sudo import sudo_users

zhunehra = clients.zhunehra
tagging_status = {}


async def is_admin(chat_id, user_id):
    try:
        part = await zhunehra(GetParticipantRequest(chat_id, user_id))
        return part.participant.admin_rights or part.participant.rank
    except:
        return False

BATCH_SIZE = 5

@zhunehra.on(events.NewMessage(pattern=r"\/tagall"))
async def stylish_tagall(event):
    sender = await event.get_sender()
    sender_id = sender.id
    if not (await is_admin(event.chat_id, event.sender_id) or sender_id in sudo_users):
        return await event.reply("**Only admins can use this command.**")

    tagging_status[event.chat_id] = True
    await event.reply("**Started tagging all users...**", buttons=[Button.inline("🛑 Stop Tagging", data=b"stop_tagging")])

    count = 0
    user_batch = []

    async for user in zhunehra.iter_participants(event.chat_id, filter=ChannelParticipantsSearch("")):
        if not tagging_status.get(event.chat_id):
            break
        if user.bot or user.deleted:
            continue

        name = user.first_name or "Friend"
        mention = f"[{name}](tg://user?id={user.id})"
        user_batch.append(mention)
        count += 1

        if len(user_batch) >= BATCH_SIZE:
            line = random.choice(tag_lines)
            msg = f"{' '.join(user_batch)}\n{line}"
            await event.reply(msg, parse_mode="md")
            user_batch.clear()
            await asyncio.sleep(2)

    if user_batch:
        line = random.choice(tag_lines)
        msg = f"{' '.join(user_batch)}\n{line}"
        await event.reply(msg, parse_mode="md")

    tagging_status[event.chat_id] = False
    await event.respond(f"**Tagging stopped or finished.**\n**Total tagged:** `{count}`")


@zhunehra.on(events.NewMessage(pattern=r"\/tagstop"))
async def manual_stop(event):
    sender = await event.get_sender()
    sender_id = sender.id
    if not (await is_admin(event.chat_id, event.sender_id) or sender_id in sudo_users):
        return await event.reply("**Only admins can stop tagging.**")

    tagging_status[event.chat_id] = False
    await event.reply("**Stopped tagging manually!**")

@zhunehra.on(events.CallbackQuery(data=b"stop_tagging"))
async def stop_tagging_button(event):
    sender = await event.get_sender()
    sender_id = sender.id
    if not (await is_admin(event.chat_id, event.sender_id) or sender_id in sudo_users):
        return await event.answer("Only admins can stop tagging.", alert=True)

    tagging_status[event.chat_id] = False
    await event.edit("**Stopped tagging!**")
