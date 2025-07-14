from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.services.app_state import set_last_api_timestamp, addLocation, setDistance
from daftlistings.daftlistings import Location, Distance
from datetime import datetime
from app.routes import daft_routes, config_routes, webpage_routes
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

set_last_api_timestamp(datetime.now())
addLocation(Location.NEWCASTLE_GALWAY)
setDistance(Distance.KM5)

app.include_router(daft_routes.router)
app.include_router(config_routes.router)
app.include_router(webpage_routes.router)