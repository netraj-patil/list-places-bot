from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.utils.logging_decorator import logging_decorator, logger
from app.services.app_state import get_last_api_timestamp, getDistance, getLocation, addLocation
from daftlistings.daftlistings import Location
from pydantic import BaseModel

# print(loc.value["displayName"])

router = APIRouter(prefix="/config", tags=["Config"])

class AddLocation(BaseModel):
    loc: str

@router.get("/get_locations")
@logging_decorator
def get_locations():
    locations = getLocation()
    loc = []
    for location in locations:
        loc.append(location.value["displayName"])
    
    return JSONResponse(
        status_code=200,
        content={
            "locations" : loc
        }
    )

@router.get("/get_distance")
@logging_decorator
def get_distance():
    distance = getDistance()
    return JSONResponse(
        status_code=200,
        content={
            "distance" : f"{distance.value} m"
        }
    )

@router.post("/add_location")
@logging_decorator
def add_location(data: AddLocation):
    found = False
    for location_member in Location:
        if location_member.value["displayValue"] == data.loc:
            addLocation(location=location_member)
            found = True
            break

    if not found:
        return JSONResponse(
            status_code=400,
            content={
                "message" : "Invalid Location recieved"
            }
        )
    
    return JSONResponse(
        status_code=200,
        content={
            "message" : "Successfully added the location"
        }
    )

@router.get("/location-selector")
@logging_decorator
def location_selector():
    locations = [
        {
            "name": loc.name,
            "id" : loc.value["id"],
            "displayName": loc.value["displayName"],
            "displayValue": loc.value["displayValue"]
        }
        for loc in Location
    ]

    return JSONResponse(
        status_code=200,
        content={
            "locations":locations
        }
    )