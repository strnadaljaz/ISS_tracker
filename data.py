from skyfield.api import load, Timescale
from skyfield.toposlib import GeographicPosition
from skyfield.sgp4lib import EarthSatellite
from skyfield.timelib import Time
from zoneinfo import ZoneInfo
from datetime import timedelta
import os
from datetime import datetime

eph = load('de421.bsp')

# loads satellites data from url and 
# searches for ISS and returns it
def getIss() -> EarthSatellite:
    satellites = load.tle_file('http://celestrak.org/NORAD/elements/stations.txt')
    by_name = {sat.name: sat for sat in satellites}
    iss = by_name['ISS (ZARYA)']

    return iss

# Gets when ISS could be visible from location 
# you specify in time window from now to 24 hours later.
# Doesn't take into account the weather conditions and 
# sun position
def getVisibleTimes(dataUrl: str, timeSystem: Timescale, location: GeographicPosition) -> tuple[list[datetime], list[int], list[Time]]:
    iss = getIss() 

    # Current time and time 24 hours later
    t0 = timeSystem.now()
    t1 = timeSystem.from_datetime(t0.utc_datetime() + timedelta(days=1))

    # Gets events and times
    # Events: - 0 for beginning
    #         - 1 for ideal position
    #         - 2 for the end of visible window
    times, events = iss.find_events(location, t0, t1, 10.0)

    # Convert times from UTC to my local times
    localTimes = []

    for t in times:
        localTime = t.utc_datetime().astimezone(ZoneInfo(os.getenv("TIMEZONE")))
        localTimes.append(localTime)

    # We also remove utc times, because we need them 
    # for further calculations, like Sun altitude
    return localTimes, events, times

# Function returns sun altitude (in degrees as a float) on specified time from
# specified location 
def getSunAltitude(time: Time, location: GeographicPosition) -> float:
    # Get sun and earth position in space
    sun = eph['sun']
    earth = eph['earth']

    # Combine earth with location specified
    earthAtLocation = earth + location

    # Calculate sun position from specified location
    sunPos = earthAtLocation.at(time).observe(sun).apparent()

    # Calculate altitude in degrees, horizontal direction (azimuth) in degrees
    # and distance from location to sun. Azimuth and distance is not needed
    # at the moment, but in the future of this project, they will be very useful 
    altitude, azimuth, distance = sunPos.altaz()

    return altitude.degrees

# Returns true if is ISS in sunlight, else returns false
def isIssInSunlight(time: Time) -> bool:
    eph = load('de421.bsp')
    iss = getIss()
    sunlit = iss.at(time).is_sunlit(eph) 

    return sunlit