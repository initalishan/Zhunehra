from os import environ
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()
api_id = int(environ["api_id"])
api_hash = environ["api_hash"]
bot_token = environ["bot_token"]

zhunehra = TelegramClient("zhunehra", api_id, api_hash).start(bot_token=bot_token)