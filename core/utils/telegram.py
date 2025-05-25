import os
import logging
import telegram
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

async def send_telegram_message(token, chat_id, text):
    if not token or not chat_id:
        logging.warning("BOT_TOKEN или CHAT_ID не заданы.")
        return
    try:
        bot = telegram.Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
        logging.info("Сообщение успешно отправлено в Telegram.")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")
