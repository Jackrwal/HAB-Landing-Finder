import requests
import time
import json


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
    range = 30

    running = False

    # How often the tracking data should be updated and filtered in seconds
    interval = 300

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
        print('retrieving latest predictions')

        HABTracker._trackData = requests.get(HABTracker.trackingURL).json()
        print(HABTracker._trackData)


#HABTracker.run()