# HAB-Landing-Finder
This python scripts uses the predictions from CUSF's HABHub hourly predictor (https://predict.habhub.org/) to predict where High altitude weather balloons will land using current wind forecasts. When run it will request these predictions and return any which are with in a given distance of a given home location, and so may be viable for you to go and collect a free radio sonde when they land :).

Note the script only reports results for potential launches at 00:00, 06:00, 12:00 and 18:00 as these are the times when Met Office balloons are normally launched, this is because the prediction just returns hourly predictions for if a balloon was to be launched, rather than only predictions for when a balloon will be launched.

If you are interested in launches not as these times you may add more launch hours to line 77 (below)<br> `if launch['hour'] == 0 or launch['hour'] == 6 or launch['hour'] == 12 or launch['hour'] == 18:`


## Install
Requirements: python3 and python3 requests library

Navigate to an empty directory where you want the script to be installed and use git clone to download the repository, or download the project ZIP and expand it here if not using git.

Install pipenv for requirements management and python virual environment using pip (pip is a package installer that comes with python):<br> `pip install pipenv`

To install project requirements and create virtual run environment:<br> `pipenv install`

Note if you wish to run the script outside of a virtual environment or to install packages not using the python package installer skip these steps and ensure the python requests libary is installed.


## Usage
Run `python getHABLandingsInDistance.py <Home Lat> <Home Long> <Distance in KM> <Predictor URL>` for predictions.

Run `python getHABLandingsInDistance.py --help` for a description of parameters.


### Linux Cron Job
This is a cron job that may be useful for running this on a linux server. This runs the script at 6am each morning for launches in Watnall, Herstmonceux and Camborne and emails a given email with any landings predicted in the given distance.

````
<min>      6       *       *       *       <folder you put HAB finder in>/HAB-Landing-Finder/getHABLandingsInDistance.py <home lat> <home lng> <distance> http://predict.habhub.org/hourly/watnall | mail --exec 'set nonullbody' -s "Watnall Sonde Predictions" <email>

<min>      6       *       *       *       <folder you put HAB finder in>/HAB-Landing-Finder/getHABLandingsInDistance.py <home lat> <home lng> <distance> http://predict.habhub.org/hourly/herstmonceux | mail --exec 'set nonullbody' -s "Herstmonceux Sonde Predictions" <email>

<min>      6       *       *       *       <folder you put HAB finder in>/HAB-Landing-Finder/getHABLandingsInDistance.py <home lat> <home lng> <distance> http://predict.habhub.org/hourly/camborne | mail --exec 'set nonullbody' -s "Camborne Sonde Predictions" <email>
`````

Note, if you download the zip you will need to rename the script's folder removing the '-master' from the end for the cron job as written above to work.
