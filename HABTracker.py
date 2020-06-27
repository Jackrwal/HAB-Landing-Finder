import requests
import time
import json
from math import radians, cos, sin, asin, sqrt

#https://www.google.com/maps/?q=<lat>,<lng>

class HABTracker:

    # I just made most these variables publicly available from outside the class (with the exception of home which needs some formatting on set)
    # i might in future make them private, prefix with '_' , and set up getters and setters
    # but this seemed like over-kill for the situation at the moment.

    # the URL from which we can retrieve the tracking data for live HABs from HabHub
    trackingURL = "https://legacy-snus.habhub.org/tracker/get_predictions.php"
    _trackData = {}

    # home location to track with-in range from in Lat and Long
    _home = {"latitude": -1, "longitude": -1}

    # range from home to track in kilometers
    range = -1

    running = False

    # How often the tracking data should be updated and filtered in seconds
    # default 5 minutes
    interval = 300

    @staticmethod
    def runOnce(lat ,lng, range):
        HABTracker._home = {"latitude": lat, "longitude": lng}
        HABTracker.range = range

        landings = HABTracker._filter()
        print(landings)


    @staticmethod
    def run():
        # Check if any parameters are un-set

        if HABTracker._home["latitude"] == -1 or HABTracker._home["longitude"] == -1:
            print("Error: Home is not set")
            return

        if HABTracker.range == -1:
            print("Error: Range is not set")
            return

        HABTracker.running = True

        while HABTracker.running:
            HABTracker._updateTrackingData()

            # Filter Data
            landings = HABTracker._filter()
            print(landings)

            # Notify for any predicted landings near by

            time.sleep(HABTracker.interval)

    @staticmethod
    def stop():
        HABTracker.running = False

    @staticmethod
    def setHome(lat, lng):
        HABTracker._home = {"latitude": lat, "longitude": lng}

    @staticmethod
    def _updateTrackingData():
        HABTracker._trackData = requests.get(HABTracker.trackingURL).json()

    @staticmethod
    def _filter():

        result = []

        for prediction in HABTracker._trackData:
            locations = json.loads(prediction["data"])

            # check for dataless responses
            if len(locations) < 1 or (type(locations) is dict and 'errors' in locations.keys()):
                continue

            # To filter on landed or descending use
            # if prediciton[<"landed" or "descending">] == <1 or 0>: continue (this skips this prediction)

            landing = locations[len(locations)-1]
            distance = HABTracker._findLandingDistance(landing)
            if distance < HABTracker.range:

                prediction["landing"] = landing
                prediction["distance"] = distance
                prediction["data"] = "processed"
                result.append(prediction)

        return result

    @staticmethod
    def _findLandingDistance(landing):

        lat1 = HABTracker._home['latitude']
        lng1 = HABTracker._home['longitude']

        lat2 = float(landing['lat'])
        lng2 = float(landing['lon'])

        # convert lat long to radians
        lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

        # Haversine formula
        dLng = lng2 - lng1
        dLat = lat2 - lat1

        a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLng / 2) ** 2
        c = 2 * asin(sqrt(a))

        # the earths radius in Km
        radius = 6371

        return c * radius

#HABTracker.runOnce(52.317445, -0.7021945, 100)
#HABTracker.run()