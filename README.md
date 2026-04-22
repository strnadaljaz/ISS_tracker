# 1. Goals of this project
In this project, my goal is to track ISS (International Space Station) location, predict when it will be visible from my location and send notification about that time to my phone. 
I also want to build small home station, which will receive data from my server through WiFi and then point to the ISS, so it will be even easier to spot from the earth.

# 2. Features
Current project features (already implemented):
- Get times when ISS will be visible (start time, optimal time and end time) for 24 hours ahead
- Then check for each time two conditions: 
    - Is sun under the horizon (it's altitude is < 0 degrees)
    - ISS is sunlit
- Times, for which are all conditions met, are then sent to my *Telegram* account with usage of their bot.
- Script that waits for a http request and sends back ISS altitude and azimuth in degrees

# 3. Requirements
Pip packages app uses:
- skyfield
- colorama
- dotenv
- requests
- fastapi

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
pip install -r requirements.txt
```

# 5. Usage
- Run script
```bash
python3 main.py
```
- Calculations for ESP32 module
```bash
python3 tracker.py
```

# 6. Configuration
If you want to run it yourself, you need to create a *.env* file, in which you put six variables:
- LATITUDE (your location latitude)
- LONGITUDE (your location longitude)
- ELEVATION (your elevation) and
- TIMEZONE (your timezone, for example "Europe/Ljubljana")

For Telegram bot purposes you also need to set (how to get them go look at their documentation): 
- BOT_API and
- CHAT_ID

# 7. Credits
Thanks to Skyfield for an amazing library! Without them, this project would be a lot harder.
Also thanks goes to Telegram for their free chat bot.