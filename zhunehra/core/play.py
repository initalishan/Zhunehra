from zhunehra.core.module_injector import *
from pytgcalls.types import AudioQuality, MediaStream

async def Play_Audio(chat_id, path):
    await Call.play(
        chat_id,
        stream=MediaStream(
            path,
            audio_parameters=AudioQuality.HIGH
            )
        )