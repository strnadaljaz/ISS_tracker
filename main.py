from skyfield.api import load, wgs84
from data import getVisibleTimes, getSunAltitude, isIssInSunlight
import os
from dotenv import load_dotenv
from send_msg import sendMessage, getMessageText

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

text = getMessageText(visible, visibleEvents)
sendMessage(text)