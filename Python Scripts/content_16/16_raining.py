import os
import sys
import requests
from bs4 import BeautifulSoup
import keyring 
from twilio.rest import Client

"""

"""

url = "https://forecast.weather.gov/MapClick.php?lat=39.050976&lon=-95.670433"
res = requests.get(url)
res.raise_for_status()

soupReader = BeautifulSoup(res.text, "html.parser")

weather_elem = soupReader.find("div",{"id": "current_conditions-summary"})

weather_status = weather_elem.find("p",{"class":"myforecast-current"}).text

if "RAIN" in str(weather_status).upper():
    twilio_sid = keyring.get_password("system", "twilio_sid")
    twilio_secret = keyring.get_password("system", twilio_sid)
    twilio_number = keyring.get_password("system", "twilio_number")
    personal_number = keyring.get_password("system", "personal_number")

    twilio_client = Client(twilio_sid,twilio_secret)

    try:
        sms = twilio_client.messages.create(
                body= "It is raining. Don't forget an umbrella",
                from_= twilio_number,
                to= personal_number
            )
        
        print(f"Message sent successfully! SID: {sms.sid}")

    except Exception as e:
        print(f"Failed to send SMS: {e}")
        sys.exit(1)

