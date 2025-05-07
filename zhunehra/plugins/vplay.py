from zhunehra.core import clients
from zhunehra.misc.queue import add_to_queue
from telethon.tl.functions.channels import GetParticipantRequest, EditBannedRequest, GetFullChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest, ImportChatInviteRequest
from telethon.errors import UserNotParticipantError, ChatAdminRequiredError, UserAlreadyParticipantError
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantBanned, ChatBannedRights
from telethon import events
from re import search
from asyncio import create_task
 
zhunehra = clients.zhunehra
assistant = clients.assistant

@zhunehra.on(events.NewMessage(pattern=r"\/vplay(?:@[\w]+)?(?:\s+(.+))?"))
async def play_handler(event):
    if event.is_private:
        return await event.reply("This command work's only groups.")
    try:
        await event.delete()
    except:
        pass
    return await event.reply("Due to server overload, video streaming is paused for now. Don't worry, we’ll be back soon!.")
    global assistant
    format = "mp4"
    user = await event.get_sender()
    try:
        mention = f"[{user.first_name}](tg://user?id={user.id})"
    except Exception:
        mention = "Anonymous"
    chat = await event.get_chat()
    chat_id = int(f"-100{chat.id}" if not str(chat.id).startswith("-100") else chat.id)
    full_channel = await zhunehra(GetFullChannelRequest(chat_id))
    call = full_channel.full_chat.call
    if not call:
        return await event.reply("Voice chat is not active.")
    me = await zhunehra.get_me()
    assistant_entity = await assistant.get_me()
    song_name = event.pattern_match.group(1)
    if not song_name:
        return await event.reply("Please provide a song name or YouTube URL after `/play`.")
    try:
        result = await zhunehra(GetParticipantRequest(chat_id, assistant_entity.id))
        assistant_status = result.participant
        if isinstance(assistant_status, ChannelParticipantBanned):
            admin_status = await zhunehra(GetParticipantRequest(chat_id, me.id))
            if isinstance(admin_status.participant, ChannelParticipantAdmin):
                admin_rights = admin_status.participant.admin_rights
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
                    await zhunehra(EditBannedRequest(chat_id, assistant_entity.id, rights))
                    if admin_rights.invite_users:
                        export_link = await zhunehra(ExportChatInviteRequest(chat_id))
                        chat_link = export_link.link
                        invite_code = search(r"(?:joinchat/|\+)([a-zA-Z0-9_-]+)", chat_link).group(1)
                        await assistant(ImportChatInviteRequest(invite_code))
                        await assistant.send_message(chat_id, "I unbanned!, Ready?, I am comming to vc.")
                        create_task(add_to_queue(song_name, chat_id, format, mention))
                    else:
                        return await event.reply("Zhunehra has no access to invite Assistant, Please gibe me (Create Invite Link) Admin rights.")
                else:
                    return await event.reply("Zhunehra has no access to unban Assistant, Please gibe me (ban rights).")
            else:
                return await event.reply("Zhunehra is not admin, Please gibe me admin with (Create Invite Link) Admin rights.")
        else:
            try:
                export_link = await zhunehra(ExportChatInviteRequest(chat_id))
            except ChatAdminRequiredError:
                return await event.reply("Zhunehra is not admin, Please gibe me admin with (Create Invite Link) Admin rights.")
            chat_link = export_link.link
            invite_code = search(r"(?:joinchat/|\+)([a-zA-Z0-9_-]+)", chat_link).group(1)
            await assistant(ImportChatInviteRequest(invite_code))
            await assistant.send_message(chat_id, "I joined!, I am comming..")
            create_task(add_to_queue(song_name, chat_id, format, mention))
    except UserNotParticipantError:
        try:
            export_link = await zhunehra(ExportChatInviteRequest(chat_id))
        except ChatAdminRequiredError:
            return await event.reply("Zhunehra has no access to invite Assistant, Please gibe me (Create Invite Link) Admin rights.")
        chat_link = export_link.link
        invite_code = search(r"(?:joinchat/|\+)([a-zA-Z0-9_-]+)", chat_link).group(1)
        await assistant(ImportChatInviteRequest(invite_code))
        await assistant.send_message(chat_id, "I joined!, I am comming..")
        create_task(add_to_queue(song_name, chat_id, format, mention))
    except UserAlreadyParticipantError:
        create_task(add_to_queue(song_name, chat_id, format, mention))
    except Exception as e:
        print(str(e))
        return await event.reply("i have not access to check my assistant in your group or not, Please make your chat history Visable, Convert to (**Super Group**).")