# HAB-Landing-Finder

This python scripts uses the predictions from CUSF's HABHub hourly predictor (https://predict.habhub.org/) to predict where High altitude wheather baloons will land using current wind forecasts. When run it will request these predictions and return any which are with in a given distance of a given home location, and so may be viable for you to go collect a free radio sonde when they land :).

note the script only reports results for potential launches at 00:00, 06:00, 12:00 and 18:00 as these are the times when baloons are normally launched, this is because the HABHub predicter just returns hourly predictions for if a baloon was to be launched, rather than only predictions for when a balloon will be launched. 

If you are interested in launches not at these times you may add more launch hours to line 77 (below)<br>
`if launch['hour'] == 0 or launch['hour'] == 6 or launch['hour'] == 12 or launch['hour'] == 18:`

## Install
Requirements: python3

to get the code navigate to an empty directory where you want the code and use git clone to download the repository or download the project ZIP and expand it here if not using git

run the following commands in a terminal in the above directory to install the script

install pipenv for requirements managment and python virual environment using pip (pip is a package installer that comes with python):<br>
`pip install pipenv`

to install project requirements and create virutal run environment:<br>
`pipenv install`

note if you wish to run the script outside of a virtual environment or to install packages not using the python package installer 
skip this step and ensure the python requests libary is installed.

## Usage
run `Python getHABLandingsInDistance.py <Home Lat> <Home Long> <distance> <URL>`

use `Python getHABLandingsInDistance.py --help` for a description of paramaters.


### Linux Cron Job
this is a cron job that may be usefull for running this on a linux server. This runs the script at 6am each morning for launches in Watnall, Herstmonceux and Camborne and emails a given email with any landings predicted that day in the given distance

````
Xx      6       *       *       *       <folder you put HAB finder in>/HAB-Landing-Finder/getHABLandingsInDistance.py <home lat> <home lng> <distance> http://predict.habhub.org/hourly/watnall | mail --exec 'set nonullbody' -s "Watnall Sonde Predictions" <email>

Xx      6       *       *       *       <folder you put HAB finder in>/HAB-Landing-Finder/getHABLandingsInDistance.py <home lat> <home lng> <distance> http://predict.habhub.org/hourly/herstmonceux | mail --exec 'set nonullbody' -s "Herstmonceux Sonde Predictions" <email>

Xx      6       *       *       *       <folder you put HAB finder in>/HAB-Landing-Finder/getHABLandingsInDistance.py <home lat> <home lng> <distance> http://predict.habhub.org/hourly/camborne | mail --exec 'set nonullbody' -s "Camborne Sonde Predictions" <email>
`````

note if you download the zip you will need to rename the script's folder removing the '-master' from the end for the cron job to work


