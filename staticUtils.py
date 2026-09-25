import csv

_stops = {}
with open("staticData/stops.txt", "r") as stopsFile:
    stopsCsv = csv.reader(stopsFile)
    _stops = {row[0]: row[1] for row in stopsCsv}
    # keys are stop IDs, values are readable names

_routes = {}
with open("staticData/routes.txt", "r") as routesFile:
    routesCsv = csv.reader(routesFile)
    _routes = {row[0]: row[3] for row in routesCsv}
    # keys are route characters, values are verbose readable names

def getRouteName(routeId):
    return _routes[routeId]

def getStopName(stopCode):
    # interestingly, some locations in the system do not map to named passenger stations.
    return _stops.get(stopCode, None)