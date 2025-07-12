import os
import requests
from app.utils.logging_decorator import logger, logging_decorator
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID =  os.getenv("PHONE_NUMBER_ID")

@logging_decorator
async def send_whatsapp_message(to_phone_number: str, message_text: str, phone_number_id: str = None):
    if not WHATSAPP_ACCESS_TOKEN:
        logger.warning("WHATSAPP_ACCESS_TOKEN not found")
    if not PHONE_NUMBER_ID:
        logger.warning("PHONE_NUMBER_ID not found")
    
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload= {
        "messaging_product" : "whatsapp",
        "to": to_phone_number,
        "type": "text",
        "text" : {
            "body": message_text
        }
    }

    try:
        response = requests.post(url=url, headers=headers, json=payload)
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"Failed to send message to {to_phone_number} : {e}")
        return False
