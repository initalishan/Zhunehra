from os import environ
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
from pytgcalls import PyTgCalls

load_dotenv()
api_id = int(environ["api_id"])
api_hash = environ["api_hash"]
bot_token = environ["bot_token"]
string_session = environ["string_session"]
zhunehra = TelegramClient("zhunehra", api_id, api_hash).start(bot_token=bot_token)
assistant = TelegramClient(StringSession(string_session), api_id, api_hash)
music = PyTgCalls(assistant)