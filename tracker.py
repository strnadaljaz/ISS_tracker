from data import getIssAltitudeAndAzimuth
from skyfield.api import load, wgs84
from dotenv import load_dotenv
from fastapi import FastAPI
import os

# Need this for the requests
app = FastAPI()

load_dotenv()

LAT = float(os.getenv("LATITUDE"))
LON = float(os.getenv("LONGITUDE"))
ELEV = float(os.getenv("ELEVATION"))

myPosition = wgs84.latlon(LAT, LON, ELEV)

timeSystem = load.timescale()

print("Server alert")

# Wait for the request from module esp32
@app.get("/iss")
def sendDataToModule():
    # Current time
    timeNow = timeSystem.now()
    print("Got request")
    # Altitude and azimuth
    alt, az = getIssAltitudeAndAzimuth(timeNow, myPosition)
    print(alt) 
    # If ISS is under horizon, we don't send data
    if alt < 0: 
        return {
            "visible": False
        }

    # If ISS is visible, we send altitude and azimuth rounded to one decimal
    return {
        "az": round(az, 1),
        "el": round(alt, 1),
        "visible": True
    }