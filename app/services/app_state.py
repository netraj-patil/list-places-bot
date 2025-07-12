from datetime import datetime
from daftlistings.daftlistings import Location, Distance

class AppState:
    def __init__(self):
        self.lastApiTimestamp = datetime.now()
        self.locations = []
        self.distance = None

appInstance = AppState()

def get_last_api_timestamp():
    return appInstance.lastApiTimestamp

def set_last_api_timestamp(setTime):
    if not isinstance(setTime, datetime):
        raise ValueError(f"Expected a datetime.datetime object. But recieved a value of type {type(setTime).__name__}")
    appInstance.lastApiTimestamp = setTime

def addLocation(location: Location):
    appInstance.locations.append(location)

def getLocation() -> list[Location]:
    return appInstance.locations

def setDistance(distance: Distance):
    appInstance.distance = distance

def getDistance() -> Distance:
    return appInstance.distance