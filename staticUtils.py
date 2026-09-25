import csv

stops = {}
with open("staticData/stops.txt", "r") as stopsFile:
    stopsCsv = csv.reader(stopsFile)
    for row in stopsCsv:
        stops[row[0]] = row[1] # keys are stop IDs, values are readable names

routes = {}
with open("staticData/routes.txt", "r") as routesFile:
    routesCsv = csv.reader(routesFile)
    for row in routesCsv:
        routes[row[0]] = row[3] # keys are route codes, values are readable names

def getRouteName(routeId):
    return routes[routeId]

def getStopName(stopCode):
    return stops.get(stopCode, None)