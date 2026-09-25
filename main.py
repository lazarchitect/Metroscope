import sys
import time
from requests import get
from datetime import datetime, timedelta, timezone
import gtfs_realtime_pb2 as subwaySchema
from staticUtils import getRouteName, getStopName

class Trip:
    def __init__(self, id):
        self.id = id
        self.vehicle = None
        self.updates = None
    def __str__(self) -> str:
        routeId = self.vehicle.trip.route_id
        routeName = getRouteName(routeId)
        return f'Trip {self.id} on {routeId} ({routeName})'

ROUTES = "-nqrw" # leave blank for 1234567S
SUBWAY_DATA_URL = f"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs{ROUTES}"

def insertVehicle(trips, vehicle):
    id = vehicle.trip.trip_id
    if id not in trips:
        trips[id] = Trip(id)
    trips[id].vehicle = vehicle

def insertUpdate(trips, tripUpdates):
    id = tripUpdates.trip.trip_id
    if id not in trips:
        trips[id] = Trip(id)
    trips[id].updates = tripUpdates

def insertAlert(trips, alert):
    pass # unspecified for now, see reference doc for structure.
    # basically an alert might reference zero or more trips

def fetchSubwayData():
    currentSubwayTripResponse = get(SUBWAY_DATA_URL)
    currentSubwayTrips = currentSubwayTripResponse.content
    feed = subwaySchema.FeedMessage()
    feed.ParseFromString(currentSubwayTrips)
    return feed

def populateTrips(feed):
    trips = {}
    entities = feed.entity # actually a list

    for entity in entities:
        if entity.HasField("trip_update"):
            insertUpdate(trips, entity.trip_update)
        if entity.HasField("alert"):
            print("ALERT!!!")
            # exit()
            insertAlert(trips, entity.alert)
        if entity.HasField("vehicle"):
            insertVehicle(trips, entity.vehicle)

    # tripsReadable = str({k: str(v) for k, v in trips.items()})
    return trips


while(True):
    trips = populateTrips(fetchSubwayData())
    iterTrips = iter(trips)
    for tripId in iterTrips:
        vehicle = trips[tripId].vehicle
        stopName = getStopName(vehicle.stop_id)
        # print(stop)
        if vehicle.current_status == 0:
            print(vehicle.current_status," ", stopName)
    time.sleep(5)