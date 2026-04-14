# 1. Goals of this project
In this project, my goal is to track ISS (International Space Station) location, predict when it will be visible from my location and send notification about that time to my phone. 
I also want to build small home station, which will receive data from my server through WiFi and then point to the ISS, so it will be even easier to spot from the earth.

# 2. Features
Current project features (already implemented):
- Get times when ISS will be visible (start time, optimal time and end time) for 24 hours ahead
- App doesn't yet take into account the position of the sun, which is very important (you can't see ISS if it's sunny outside)
- Script converts UTC time of visibility to my local time.

# 3. Requirements
Pip packages app uses:
- skyfield
- colorama
- dotenv

# 4. Installation
- Clone repo
```bash
git clone https://github.com/strnadaljaz/ISS_tracker.git
```

- Create virtual environment
```bash
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
```

- Install dependencies
```bash
pip install skyfield colorama python-dotenv
```

# 5. Usage
- Run script
```bash
python3 tracker.py
```

# 6. Configuration
If you want to set your location, you need to create a *.env* file, in which you put four variables:
- LATITUDE (your location latitude)
- LONGITUDE (your location longitude)
- ELEVATION (your elevation)
- TIMEZONE (your timezone, for example "Europe/Ljubljana")

# 7. Credits
Thanks to Skyfield for an amazing library! Without them, this project would be a lot harder