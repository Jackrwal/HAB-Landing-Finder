#!/usr/bin/python3

import requests
import argparse
import datetime
from math import radians, cos, sin, asin, sqrt


# Get distance between two positions in km
def haversine(lat1, lng1, lat2, lng2):
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

# Get Arguments
argParser = argparse.ArgumentParser()

argParser.add_argument('lat',
                       metavar='la',
                       type=float,
                       help="The Latitude of home location e.g. 47.3387486"
                       )

argParser.add_argument('long',
                       metavar='ln',
                       type=float,
                       help="The Longitude of home location e.g. 13.6326257"
                       )

argParser.add_argument('distance',
                       metavar='d',
                       type=int,
                       help='The max distance from home in km'
                       )

argParser.add_argument('url',
                       metavar='u',
                       type=str,
                       help='The URL to request predictions from, based on launch location ie: http://predict.habhub.org/hourly/watnall'
                       )

args = argParser.parse_args()

home = {'latitude': args.lat, 'longitude':  args.long}

# get url for manifest containing landing predictions
HABHubPredictorURL = args.url
ManifestURL = HABHubPredictorURL + '/manifest.json'

# send GET request to HabHub for manifest JSON
responseJSON = requests.get(ManifestURL).json()
predictions = responseJSON['predictions']

# Build list of near-by landings
output = ""
for prediction in predictions.values():

    landing = prediction['landing-location']
    landingDist = haversine(home['latitude'], home['longitude'], landing['latitude'], landing['longitude'])

    if landingDist <= args.distance:

        launch = prediction['launch-time']
        launchStr = "{:02d}/{:02d}/{:02d}".format(launch['day'], launch['month'], launch['year'])

        if launch['hour'] == 0 or launch['hour'] == 6 or launch['hour'] == 12 or launch['hour'] == 18:

            landing = prediction['landing-time']
            location = prediction['landing-location']

            output += "Distance: {:2.0f}km, Launch: {} {} {:02d}:{:02d}, Landing: {:02d}:{:02d}, At: https://www.google.com/maps/dir/{:2.6f},{:2.6f}/{:2.6f},{:2.6f}\n\r".format(
                landingDist,
                datetime.datetime.strptime(launchStr, '%d/%m/%Y').strftime('%a'),
                launchStr, launch['hour'], launch['minute'],
                landing['hour'], landing['minute'],
                home['latitude'], home['longitude'],
                location['latitude'], location['longitude']
            )

# If any landings were in range output these
if len(output) > 0:

    # get model date time. note model date provided in JSON is in american format
    model = responseJSON["model"]
    model = '{}/{}/{} {}:00'.format(model[6:8], model[4:6], model[:4], model[-2:])

    print('Predictions for within {:d}km of home from {} Using model {}.\n\r'.format(args.distance, args.url, model))
    print(output)
