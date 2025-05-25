import os
import logging
import telegram
import asyncio
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')

async def send_telegram_message(text):
    if not BOT_TOKEN or not CHAT_ID:
        logging.warning("BOT_TOKEN или CHAT_ID не заданы.")
        return
    try:
        bot = telegram.Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")
