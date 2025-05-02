from pytgcalls.types import AudioQuality, MediaStream
from zhunehra.core import clients

music = clients.music

async def Play_Audio(chat_id, path):
    await music.play(
        chat_id,
        stream=MediaStream(
            path,
            audio_parameters=AudioQuality.HIGH
            )
        )