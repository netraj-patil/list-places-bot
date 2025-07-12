from daftlistings.daftlistings import Daft, SortType
from fastapi import APIRouter
from datetime import datetime
import os
from dotenv import load_dotenv

from app.services.app_state import get_last_api_timestamp, getLocation, getDistance, set_last_api_timestamp
from app.services.whatsapp_services import send_whatsapp_message
from app.utils.logging_decorator import logger, logging_decorator

load_dotenv()

router = APIRouter(prefix="/daft_route", tags=["Daft Routes"])

PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
RECIPIENT_PHONE_NUMBERS = os.getenv("RECIPIENT_PHONE_NUMBERS")

@logging_decorator
def postings_after_timestamp():
    daft = Daft()
    
    last_api_timestamp = get_last_api_timestamp()
    locations = getLocation()
    distance = getDistance()

    daft.set_location(locations, distance=distance)
    daft.set_sort_type(SortType.PUBLISH_DATE_DESC)
    listings = daft.search()

    results = []

    date_format = "%Y-%m-%d %H:%M:%S.%f"

    for listing in listings:
        publish_datetime = datetime.strptime(listing.publish_date, date_format)
        if publish_datetime < last_api_timestamp:
            break
        results.append(
            {
                "location" : listing.title,
                "price": listing.price,
                "url": listing.daft_link,
                "published_time": listing.publish_date
            }
        )
    
    set_last_api_timestamp(datetime.now())
    
    return results

@router.get("/get_recent_postings")
@logging_decorator
def get_recent_postings():
    if not RECIPIENT_PHONE_NUMBERS:
        logger.warning("Recipient phone numbers not found")
        raise ValueError("Recipient phone numbers not found")
    
    if not PHONE_NUMBER_ID:
        logger.warning("Phone number ID not found")
        raise ValueError("Phone number ID not found")
    
    results = postings_after_timestamp()

    if results:
        for result in results:
            message = f"""
                Location : {result['location']}
                Price : {result['price']}
                Published Time : {result['published_time']}
                URL : {result['url']}
            """

            for to_phone_number in RECIPIENT_PHONE_NUMBERS:
                send_whatsapp_message(to_phone_number=to_phone_number, message_text=message, phone_number_id=PHONE_NUMBER_ID)
