from zhunehra.core import clients
from zhunehra.core.safedict import SafeDict
from zhunehra.utils.help import *
from zhunehra.utils.start import start_buttons
from config.strings import *
from telethon import events

zhunehra = clients.zhunehra

@zhunehra.on(events.CallbackQuery(data=b"help_menu"))
async def Help_Callback(event):
    await event.edit(
        help_caption,
        buttons=help_buttons
    )
    
@zhunehra.on(events.CallbackQuery(data=b"commands"))
async def commands_callback(event):
    await event.edit(
        command_caption,
        buttons=commands_button
    )
    
@zhunehra.on(events.CallbackQuery(data=b"back_to_start"))
async def back_to_start_callback(event):
    global start_caption
    sender = await event.get_sender()
    sender_id = event.sender.id
    username = sender.username
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
    caption = start_caption.format_map(safe_data)
    await event.edit(
        caption,
        buttons=start_buttons
    )
@zhunehra.on(events.CallbackQuery(data=b"back_to_help"))
async def back_to_help_callback(event):
    await event.edit(
        help_caption,
        buttons=help_buttons
    )
@zhunehra.on(events.CallbackQuery(data=b"about_zhunehra"))
async def about_zhunehra_callback(event):
    await event.edit(
        about_zhunehra_caption,
        buttons=about_zhunehra_buttons
    )
@zhunehra.on(events.CallbackQuery(data=b"back_to_commands"))
async def back_to_commands_callback(event):
    await event.edit(
        command_caption,
        buttons=commands_button
    )
@zhunehra.on(events.CallbackQuery(data=b"play_command"))
async def play_button_callback(event):
    await event.edit(
        play_command_caption,
        buttons=back_to_commands_button
    )
@zhunehra.on(events.CallbackQuery(data=b"vplay_command"))
async def vplay_button_callback(event):
    await event.edit(
        vplay_command_caption,
        buttons=back_to_commands_button
    )
@zhunehra.on(events.CallbackQuery(data=b"stop_command"))
async def stop_button_callback(event):
    await event.edit(
        stop_command_caption,
        buttons=back_to_commands_button
    )
@zhunehra.on(events.CallbackQuery(data=b"skip_command"))
async def skip_button_callback(event):
    await event.edit(
        skip_command_caption,
        buttons=back_to_commands_button
    )
@zhunehra.on(events.CallbackQuery(data=b"pause_command"))
async def pause_button_callback(event):
    await event.edit(
        pause_command_caption,
        buttons=back_to_commands_button
    )
@zhunehra.on(events.CallbackQuery(data=b"resume_command"))
async def resume_button_callback(event):
    await event.edit(
        resume_command_caption,
        buttons=back_to_commands_button
    )
@zhunehra.on(events.CallbackQuery(data=b"replay_command"))
async def replay_button_callback(event):
    await event.edit(
        replay_command_caption,
        buttons=back_to_commands_button
    )
@zhunehra.on(events.CallbackQuery(data=b"download_command"))
async def download_button_callback(event):
    await event.edit(
        download_command_caption,
        buttons=back_to_commands_button
    )
@zhunehra.on(events.CallbackQuery(data=b"welcome_command"))
async def welcome_button_callback(event):
    await event.edit(
        welcome_command_caption,
        buttons=back_to_commands_button
    )
    
@zhunehra.on(events.CallbackQuery(data=b"commands_2"))
async def commands_2_callback(event):
    await event.edit(
        command_caption,
        buttons=commands_button_2
    )
@zhunehra.on(events.CallbackQuery(data=b"back_to_commands_2"))
async def back_to_commands_2_callback(event):
    await event.edit(
        command_caption,
        buttons=commands_button_2
    )
@zhunehra.on(events.CallbackQuery(data=b"truth&dare"))
async def truth_and_dare_callback(event):
    await event.edit(
        truth_and_dare_command_caption,
        buttons=back_to_commands_2_button
    )