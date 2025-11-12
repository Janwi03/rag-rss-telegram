from telegram import Bot
import asyncio

# Replace this with your actual token
TELEGRAM_BOT_TOKEN = "8255221582:AAFCtIJnWeqvWI-wYDqZvyXhtP5OkaHdcMM"

# Replace with your chat ID (you’ll get it in the next step)
CHAT_ID = "1565168706"

async def send_message():
    bot = Bot(token = TELEGRAM_BOT_TOKEN)
    message = "Hello! 🤖 Your RSS summarizer bot is working!"
    await bot.send_message(chat_id=CHAT_ID, text=message)
    print("✅ Message sent successfully!")

if __name__ == "__main__":
    asyncio.run(send_message())