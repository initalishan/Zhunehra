from zhunehra.core import clients

music = clients.music

async def Play_Audio(chat_id, path):
    try:
        await music.play(chat_id, path)
    except:
        pass