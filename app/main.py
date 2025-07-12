from fastapi import FastAPI
from app.services.app_state import set_last_api_timestamp, addLocation, setDistance
from daftlistings.daftlistings import Location, Distance
from datetime import datetime
from app.routes import daft_routes
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

set_last_api_timestamp(datetime.now())
addLocation(Location.NEWCASTLE_DUBLIN)
setDistance(Distance.KM5)

app.include_router(daft_routes.router)