from gtts import gTTS
import pygame, pyttsx3
import requests, json, datetime, pytz
from dateutil import parser
from io import BytesIO

AW_KEY      = "PlYNYwY61E9c7YOJyoZfYDEFEGwywR71"
LOCATION    = "3146227"
url         = f"http://dataservice.accuweather.com/currentconditions/v1/{LOCATION}?apikey={AW_KEY}"

insightful_statement = f"Greetings! It's 7:00 PM, the weather in NOIDA is 31°, partly cloudy with low chances of precipitation."

pygame.mixer.init()

response = requests.get(url)
if response.status_code == 200:
    data = response.json()[0]
    with open("response.json", "w") as fw:
        json.dump(data, fw)
    weather_text = data["WeatherText"]
    has_precipitation = data["HasPrecipitation"]
    temperature_celsius = data["Temperature"]["Metric"]["Value"]

    timestamp = parser.parse(data["LocalObservationDateTime"])

    observation_time = timestamp.strftime("%I:%M %p")

    local_time = timestamp.astimezone(pytz.timezone('Asia/Kolkata'))

    if has_precipitation:
        precipitation_status = "with precipitation"
    else:
        precipitation_status = "without precipitation"

    insightful_statement = f"Greetings! It's {observation_time}, the weather in NOIDA is {temperature_celsius}°, {weather_text} {precipitation_status}."

else:
    print(response.status_code)

tts = gTTS(insightful_statement, lang='en', tld="co.in")
tts.save("output.mp3")

print(insightful_statement)
pygame.mixer.music.load("output.mp3")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pass

pygame.quit()
