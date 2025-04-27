from telethon import TelegramClient, Button

api_id = 27684245
api_hash = "22c33e48a7697c767c5e40bda82a8db9"
bot_token = "8056248042:AAHF7CobDP3NfDCnw9q2NEReIxWpTdUe-6A"
target_chat_id = 7872695556
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def send_promotion_message():
    message = """
🎶 **Introducing Zhunehra - The Ultimate Music Bot!** 🎶

Looking for a bot that can play your favorite music effortlessly in your Telegram groups? Look no further! **Zhunehra** is here to deliver the best music experience! 🎧

💥 **Why Zhunehra?**
- Super Fast and Reliable
- Continuous updates and improvements 🔥

🔗 **Add Zhunehra to your group NOW and start enjoying music right away!**

📱 **Bot Username**: @zhunehra_bot  
🔊 **Join our Update Channel**: @zhunehra  
🛠️ **Need help? Join the Report Group**: @zhunehra_chat
    """
    button = Button.url("Add me to your group", "http://t.me/zhunehra_bot?startgroup=botstart")
    await client.send_message(target_chat_id, message, buttons=[button])
async def main():
    await send_promotion_message()

client.loop.run_until_complete(main())