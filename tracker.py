from skyfield.api import load, wgs84
import time
from data import getVisibleTimes, getSunAltitude, isIssInSunlight
from colorama import Fore, Style, init
import os
from dotenv import load_dotenv

init()
load_dotenv()

LAT = float(os.getenv("LATITUDE"))
LON = float(os.getenv("LONGITUDE"))
ELEV = float(os.getenv("ELEVATION"))

myPosition = wgs84.latlon(LAT, LON, ELEV)

url = 'http://celestrak.org/NORAD/elements/stations.txt'

timeSystem = load.timescale()

localTimes, events, times = getVisibleTimes(url, timeSystem, myPosition)

visible = []
visibleEvents = []

for i in range(len(times)):
    altitude = getSunAltitude(times[i], myPosition)
    if altitude < 0 and isIssInSunlight:
        visible.append(localTimes[i])
        visibleEvents.append(events[i])

for i in range(len(visible)):
    if visibleEvents[i] == 0:
        print(Fore.YELLOW + "Start:" + str(visible[i]))
    elif visibleEvents[i] == 1:
        print(Fore.GREEN + "Ideal:" + str(visible[i]))
    else:
        print(Fore.RED + "End:" + str(visible[i]))