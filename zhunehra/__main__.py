print("Loading core system.")
import importlib
import os
from zhunehra.core import clients
from dotenv import load_dotenv
from asyncio import get_event_loop
import zhunehra.__init__
from zhunehra.LOGS import logs

zhunehra = clients.zhunehra
music = clients.music
assistant = clients.assistant
cookies = "cookies/cookies.txt"

load_dotenv()

async def main():
    print("Checking cookies...")
    if not os.path.exists(cookies):
        return print("Cookies not exists error. Please load cookies.txt in cookies Folder.")
    print("Cookies loaded succesfully.")
    print("Starting PyTgCalls client.")
    await music.start()
    print("PyTgCalls client succesfully started.")
    print("Checking for log group.")
    try:
        log_id = int(os.environ["chat_log"])
        print("Log group loaded succesfully.")
    except Exception:
        return print("Log chat was not found please gibe me log_chat id in .env file.")
    print("Checking for MongoDB..")
    try:
        os.environ["mongo_db_url"]
        print("Mongo db loaded succesfully.")
    except Exception:
        return print("Mongo db was not found please gibe me mongo db url in .env file.")
    import_plugins()
    print("Starting zhunehra..")
    print("Starting Zhunehra bot..")
    try:
        await zhunehra.send_message(log_id, "**Zhunehra Started.**")
    except Exception:
       return print("Please add Zhunehra to your log group, and make her admin.")
    print("Zhunehra bot started.")
    print("Starting zhunehra assistant")
    try: 
        await music.play(log_id, "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4")
        await assistant.send_message(log_id, "**Zhunehra assistant started.**")
    except Exception:
        return print("Please add zhunehra's assistant your log group, and make her admin. And make sure log group voice chat is active")
    print("Zhunehra assistant started.")
    print("Zhunehra started.")
    await music.leave_call(log_id)
    await zhunehra.run_until_disconnected()
    
def import_plugins():
    path = "zhunehra/plugins"
    for file in os.listdir(path):
        if file.endswith(".py") and not file.startswith("__"):
            importlib.import_module(f"zhunehra.plugins.{file[:-3]}")
            print(f"{file[:-3]} plugin loaded succesfully.")
            
loop = get_event_loop()
loop.run_until_complete(main())
