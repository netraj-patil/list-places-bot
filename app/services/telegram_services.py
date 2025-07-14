import requests
from app.utils.logging_decorator import logger, logging_decorator
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@logging_decorator
async def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(
            url,
            data=payload
        )

        if response.status_code == 200:
            logger.info("Sent the message to telegram")
        else:
            logger.error("Error sending message to telegram")
    except Exception as e:
        logger.error(f"Error occurred while sending message to telegram : {e}")
        raise