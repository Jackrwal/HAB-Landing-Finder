# HAB-Landing-Finder

This python script uses the predictions from CUSF's HABHub hourly predictor (https://predict.habhub.org/) to predict where high altitude weather balloons will land using current wind forecasts. When run, the script will request these predictions and return any which are within a given distance of a given home location, and so may be viable for you to go collect a free radio sonde when they land :).

Note the script only reports results for potential launches at 00:00, 06:00, 12:00 and 18:00, at these times the Met Office launch balloons. The HABHub predictor returns predictions every hour for if a balloon was to be launched, rather than only predictions for when a balloon will be launched.

If you are interested in launches at other times you may add more launch hours to line 77 (below)<br>
`if launch['hour'] == 0 or launch['hour'] == 6 or launch['hour'] == 12 or launch['hour'] == 18:`

## Install
Requirements: python3

To get the code, navigate to the directory you wish to install the script in. Then use 'git clone https://github.com/Jackrwal/HAB-Landing-Finder' to download the repository or download the project ZIP, move it to your directory, and expand it.

Install pipenv for requirements management and python virtual environment using pip (pip is a package installer that comes with python):<br>
`pip install pipenv`

To install project requirements and create virtual run environment:<br>
`pipenv install`

Note if you wish to run the script outside of a virtual environment or to install packages not using the python package installer 
skip this step and ensure the python requests library is installed.

## Usage
run `Python getHABLandingsInDistance.py <Home Lat> <Home Long> <distance> <URL>`

Distance from home is measured in kilometres.
URL is the URL of the habhub endpoint to use for predictions<br>
e.g. http://predict.habhub.org/hourly/watnall/

run `Python getHABLandingsInDistance.py --help` for further description of parameters.

### Linux Cron Job
This is a cron job that may be useful for running this on a Linux server. This runs the script at 6am each morning for launches in Watnall, Herstmonceux and Camborne and emails a given email with any landings predicted that day in the given distance.

````
Xx      6       *       *       *       <folder you put HAB finder in>/HAB-Landing-Finder/getHABLandingsInDistance.py <home lat> <home lng> <distance> http://predict.habhub.org/hourly/watnall | mail --exec 'set nonullbody' -s "Watnall Sonde Predictions" <email>

Xx      6       *       *       *       <folder you put HAB finder in>/HAB-Landing-Finder/getHABLandingsInDistance.py <home lat> <home lng> <distance> http://predict.habhub.org/hourly/herstmonceux | mail --exec 'set nonullbody' -s "Herstmonceux Sonde Predictions" <email>

Xx      6       *       *       *       <folder you put HAB finder in>/HAB-Landing-Finder/getHABLandingsInDistance.py <home lat> <home lng> <distance> http://predict.habhub.org/hourly/camborne | mail --exec 'set nonullbody' -s "Camborne Sonde Predictions" <email>
`````

Note if you download the zip you will need to rename the script's folder removing the '-master' from the end for the above stated to work.


