from zhunehra.core.module_injector import *


class stop:
    @zhunehra.on(events.NewMessage(pattern=r"\/end"))
    async def stop(event):
        