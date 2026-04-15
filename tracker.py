from skyfield.api import load, wgs84
import time
from data import getVisibleTimes, getSunAltitude 
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

localTimes, events = getVisibleTimes(url, timeSystem, myPosition)

'''
for i in range(len(localTimes)):
    
    if events[i] == 0:
        print(Fore.YELLOW + "Start:" + str(localTimes[i]))
    elif events[i] == 1:
        print(Fore.GREEN + "Ideal:" + str(localTimes[i]))
    else:
        print(Fore.RED + "End:" + str(localTimes[i]))
'''
'''
while (True):
    if gotData:
        time.sleep(600)

    else:
        localTimes = getData(url, timeSystem, myPosition)
'''