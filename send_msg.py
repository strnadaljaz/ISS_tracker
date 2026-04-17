import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TOKEN = str(os.getenv("BOT_API"))
CHAT_ID = int(os.getenv("CHAT_ID")) 

def getMessageText(visibleTimes: list[datetime], events: list[int]) -> str:
    string = ""

    for i in range(len(visibleTimes)):
        if events[i] == 0:
            string += "Start: "
        elif events[i] == 1:
            string += "Ideal: "
        else:
            string += "End: "
        
        string += str(visibleTimes[i]) + '\n'
    
    return string

def sendMessage(text: str) -> None: 
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)