from zhunehra.core.module_injector import *


@zhunehra.on(events.CallbackQuery(data=b"help_menu"))
async def help_callback(event):
    await event.edit(
        "**Zhunehra's Help Menu**\n\n"
    )