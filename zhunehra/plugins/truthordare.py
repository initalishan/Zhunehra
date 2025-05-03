from zhunehra.core import clients
from telethon import events, Button
import requests

zhunehra = clients.zhunehra

@zhunehra.on(events.NewMessage(pattern=r"\/truth"))
async def truth_handler(event):
    response = requests.get("https://api.truthordarebot.xyz/api/truth")
    if response.status_code == 200:
        question = response.json().get("question")
        await event.reply(f"**Truth:**\n{question}",buttons=[Button.inline("Next Truth", data=b"next_truth")])
    else:
        await event.reply("Unable to fetch a truth question at the moment.")

@zhunehra.on(events.NewMessage(pattern=r"\/dare"))
async def dare_handler(event):
    response = requests.get("https://api.truthordarebot.xyz/api/dare")
    if response.status_code == 200:
        question = response.json().get("question")
        await event.reply(f"**Dare:**\n{question}", buttons=[Button.inline("Next Dare", data=b"next_dare")])
    else:
        await event.reply("Unable to fet ch a dare question at the moment.",)
        
@zhunehra.on(events.CallbackQuery(data=b'next_truth'))
async def next_truth_callback(event):
    response = requests.get("https://api.truthordarebot.xyz/api/truth")
    if response.status_code == 200:
        question = response.json().get("question")
        await event.reply(f"**Truth:**\n{question}",buttons=[Button.inline("Next Truth", data=b"next_truth")])
    else:
        await event.reply("Unable to fetch a truth question at the moment.")
        
@zhunehra.on(events.CallbackQuery(data=b'next_dare'))
async def next_dare_callback(event):
    response = requests.get("https://api.truthordarebot.xyz/api/dare")
    if response.status_code == 200:
        question = response.json().get("question")
        await event.reply(f"**Dare:**\n{question}", buttons=[Button.inline("Next Dare", data=b"next_dare")])
    else:
        await event.reply("Unable to fetch a dare question at the moment.",)