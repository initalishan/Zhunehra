from zhunehra.core.module_injector import *
from zhunehra.core.metadata import meta_data
from zhunehra.plugins.queue import add_to_queue
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.messages import ExportChatInviteRequest, ImportChatInviteRequest
from telethon.errors import ChatAdminRequiredError, UserAlreadyParticipantError, InviteHashExpiredError, UserNotParticipantError
from telethon.tl.types import ChannelParticipantBanned, ChannelParticipantLeft
from dotenv import load_dotenv 
from os import environ

load_dotenv()
assistant_id = int(environ["assistant_id"])

class Play:
    @zhunehra.on(events.NewMessage(pattern=r"/play(?:\s+(.*))?"))
    async def Play_Handler(event):
        chat_id = None
        global assistant_id
        if event.is_group:
            song_name = event.pattern_match.group(1)
            try:
                await event.delete()
            except Exception:
                pass
            sender = await event.get_sender()
            mention = f"[{sender.first_name}](tg://user?id={sender.id})"
            chat = await event.get_chat()
            if hasattr(chat, "id"):
                raw_id = chat.id
            if getattr(chat, "broadcast", False) or getattr(chat, "megagroup", False):
                if str(raw_id).startswith("-100"):
                    chat_id = raw_id
                else:
                    chat_id = int(f"-100{abs(raw_id)}")

            try:
                me = await zhunehra.get_permissions(chat_id, 'me')
            except Exception as e:
                return await event.reply("Could not fetch bot permissions. Make sure I'm an admin.")

            if not me.is_admin:
                return await event.reply("Zhunehra not an admin. Please make me admin with invite permissions.")

            if not me.invite_users:
                return await event.reply("Please give me 'Add Users via Link' permission.")

            try:
                assistant_entity = await client.get_entity("me")
                participant = await zhunehra(GetParticipantRequest(chat_id, assistant_entity))
                user_status = participant.participant
                if isinstance(user_status, (ChannelParticipantBanned, ChannelParticipantLeft)):
                    return await event.reply("Zhunera's Assistant is not in the group or has been banned. Unban or re-add the assistant.")
            except UserNotParticipantError:
                try:
                    invite = await zhunehra(ExportChatInviteRequest(chat_id))
                    invite_link = invite.link.split("/")[-1].replace("+", "")
                    await client(ImportChatInviteRequest(invite_link))
                    await client.send_message(chat_id, "Wohh, I am joined!.")
                except ChatAdminRequiredError:
                    return await event.reply("Zhunehra don't have permission to generate invite link.")
                except InviteHashExpiredError:
                    return await event.reply("The invite link has expired or is invalid.")
                except Exception as e:
                    return await event.reply(f"Failed to add assistant: {e}")
            except UserAlreadyParticipantError:
                pass
            if not song_name:
                return await event.reply("Please provide a audio name or Youtube url after`/play`.")
            status = await event.reply("Searching for song...")
            await add_to_queue(song_name, chat_id, mention)
            await status.delete()
        else:
            await event.reply("This command only works in groups.")
