from zhunehra.core import clients
from zhunehra.misc.queue import add_to_queue
from telethon.tl.functions.channels import GetParticipantRequest, EditBannedRequest, GetFullChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest, ImportChatInviteRequest
from telethon.errors import UserNotParticipantError, ChatAdminRequiredError
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantBanned, ChatBannedRights, InputPeerUser
from telethon import events
from dotenv import load_dotenv
from os import environ
 
zhunehra = clients.zhunehra
assistant = clients.assistant 
load_dotenv()
assistant_id = int(environ["assistant_id"])

@zhunehra.on(events.NewMessage(pattern=r"\/vplay(?:@[\w]+)?(?:\s+(.+))?"))
async def vplay_handler(event):
    global assistant_id
    format = "mp4"
    mention = ""
    user = await event.get_sender()
    try:
        mention = f"[{user.first_name}](tg://user?id={user.id})"
    except Exception:
        mention = "Anonymous"
    if event.is_private:
        return await event.reply("This command works only in groups.")
    song_name = event.pattern_match.group(1)
    if not song_name:
        return await event.reply("Please provide a song name or YouTube URL after `/play`.")
    try:
        await event.delete()
    except Exception: 
        pass
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
    me = await zhunehra.get_me()
    try:
        participant = await zhunehra(GetParticipantRequest(chat_id, me.id))
        if not isinstance(participant.participant, ChannelParticipantAdmin):
            return await event.reply("Zhunehra is not an admin in this group.")
    except UserNotParticipantError:
        return await event.reply("Zhunehra is not in this group.")
    except ChatAdminRequiredError:
        return await event.reply("Zhunehra is not an admin in this group.")
    try:
        try:
            assistant_entity = await zhunehra.get_input_entity(assistant_id)
        except Exception:
            assistant_user = await assistant.get_entity(assistant_id)
            assistant_entity = InputPeerUser(assistant_user.id, assistant_user.access_hash)
        result = await zhunehra(GetParticipantRequest(chat_id, assistant_entity))
        assistant_status = result.participant
        if isinstance(assistant_status, ChannelParticipantBanned):
            me = await zhunehra.get_me()
            owner = await zhunehra(GetParticipantRequest(chat_id, me.id))
            if isinstance(owner.participant, ChannelParticipantAdmin):
                admin_rights = owner.participant.admin_rights
                if admin_rights.ban_users:
                    rights = ChatBannedRights(
                        until_date=0,
                        view_messages=False,
                        send_messages=False,
                        send_media=False,
                        send_stickers=False,
                        send_gifs=False,
                        send_games=False,
                        send_inline=False,
                        embed_links=False,
                    )
                    await zhunehra(EditBannedRequest(chat_id, assistant_id, rights))
                    me = await zhunehra.get_me()
                    try:
                        participant = await zhunehra(GetParticipantRequest(chat_id, me.id))
                        if not isinstance(participant.participant, ChannelParticipantAdmin):
                            return await event.reply("Zhunehra is not an admin in this group.")
                        admin_rights = participant.participant.admin_rights
                        if admin_rights.invite_users:
                            result = await zhunehra(ExportChatInviteRequest(chat_id))
                            invite_link = result.link
                            invite_hash = invite_link.split("/")[-1].replace("+", "")
                            await assistant(ImportChatInviteRequest(invite_hash))
                            await assistant.send_message(chat_id, "/start@zhunehra_bot")
                        else:
                            return await event.reply("Zhunehra can't invite the assistant (no rights).")
                    except ChatAdminRequiredError:
                        return await event.reply("Zhunehra is not an admin in this group.")
                    await event.reply("Assistant was banned, unbanned successfully.")
                else:
                    return await event.reply("Zhunehra has no access to unban the assistant.")
    except UserNotParticipantError:
        try:
            me = await zhunehra.get_me()
            owner = await zhunehra(GetParticipantRequest(chat_id, me.id))
            if isinstance(owner.participant, ChannelParticipantAdmin):
                admin_rights = owner.participant.admin_rights
                if admin_rights.invite_users:
                    result = await zhunehra(ExportChatInviteRequest(chat_id))
                    invite_link = result.link
                    invite_hash = invite_link.split("/")[-1].replace("+", "")
                    await assistant(ImportChatInviteRequest(invite_hash))
                    await assistant.send_message(chat_id, "/start@zhunehra_bot")
                else:
                    return await event.reply("Zhunehra can't invite the assistant (no rights).")
        except ChatAdminRequiredError:
            return await event.reply("Zhunehra is not an admin in this group.")
    except Exception as e:
        return await event.reply(f"Please convert your group to **supergroup** first.")
    full_channel = await zhunehra(GetFullChannelRequest(chat_id))
    call = full_channel.full_chat.call
    if not call:
        return await event.reply("Voice chat is not active.")
    await add_to_queue(song_name, chat_id, format, mention)