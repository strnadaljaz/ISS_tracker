from skyfield.api import load
from zoneinfo import ZoneInfo
from datetime import timedelta
from dotenv import load_dotenv
import os

# Gets when ISS could be visible from location 
# you specify in time window from now to 24 hours later.
# Doesn't take into account the weather conditions and 
# sun position
def getData(dataUrl: str, timeSystem, location):
    
    # loads satellites data from url and 
    # searches for ISS
    satellites = load.tle_file(dataUrl)
    by_name = {sat.name: sat for sat in satellites}
    iss = by_name['ISS (ZARYA)']

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

    return localTimes, events