import time
from requests import get
import gtfs_realtime_pb2 as subwaySchema
from staticUtils import getRouteName, getStopName

StationStatus = {v: k for k, v in subwaySchema.VehiclePosition.VehicleStopStatus.items()}

class Trip:
    def __init__(self, id):
        
        # high level objects
        self.vehicle = None
        self.updates = None

        # extracted datapoints
        self.id = id
        self.status = None
        self.station = None

    def __str__(self) -> str:
        routeId = self.vehicle.trip.route_id
        routeName = getRouteName(routeId)
        return f'Trip {self.id} on {routeId} ({routeName}) {self.status} {self.station}'

ROUTES = "-ace" # leave blank for 1234567S
SUBWAY_DATA_URL = f"https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs{ROUTES}"

def insertVehicle(trips, vehicle):
    id = vehicle.trip.trip_id
    if id not in trips:
        trips[id] = Trip(id)
    trips[id].vehicle = vehicle
    trips[id].status = StationStatus[vehicle.current_status]
    trips[id].station = getStopName(vehicle.stop_id) # TODO verify that vehicle.stop_id matches trip_update[0].stop_id. Yeah I dont think the station referenced in the Vehicle data is always correct (seems to be the issue where the train hasnt left the origin terminus yet)

def insertUpdate(trips, tripUpdates):
    id = tripUpdates.trip.trip_id
    if id not in trips:
        trips[id] = Trip(id)
    trips[id].updates = tripUpdates

def insertAlert(trips, alert):
    print(alert)
    pass # unspecified for now, see reference doc for structure.
    # basically an alert might reference zero or more trips

def fetchSubwayData() -> FeedMessage:
    currentSubwayTripResponse = get(SUBWAY_DATA_URL)
    currentSubwayTrips = currentSubwayTripResponse.content
    feed = subwaySchema.FeedMessage()
    feed.ParseFromString(currentSubwayTrips)
    return feed

def populateTrips(feed) -> dict:
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
    return trips

while(True):
    trips = populateTrips(fetchSubwayData())
    tripsReadable = str({k: str(v) for k, v in trips.items()})
    
    for trip in trips.items():
        upcomingStopUpdates = trip[1].updates.stop_time_update
        print(str(trip[1]))
        for stopAhead in upcomingStopUpdates:
            print(getStopName(stopAhead.stop_id))
        print("---\n\n")

    time.sleep(5)