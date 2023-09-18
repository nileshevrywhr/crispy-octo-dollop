from gtts import gTTS
import pygame, pyttsx3
import requests, json

AW_KEY = "PlYNYwY61E9c7YOJyoZfYDEFEGwywR71"
LOCATION = "3146227"

url = f"http://dataservice.accuweather.com/currentconditions/v1/{LOCATION}?apikey={AW_KEY}"

# Initialize the Pygame mixer
pygame.mixer.init()

response = requests.get(url)
if response.ok:
    data = response.json()[0]
    with open("response.json", "w") as fw:
        json.dump(data, fw)
    # Extract relevant data
    observation_time = data["LocalObservationDateTime"]
    weather_text = data["WeatherText"]
    has_precipitation = data["HasPrecipitation"]
    temperature_celsius = data["Temperature"]["Metric"]["Value"]

    # Create an insightful statement
    if has_precipitation:
        precipitation_status = "with precipitation"
    else:
        precipitation_status = "without precipitation"

    insightful_statement = f"At {observation_time}, the weather in Noida is {weather_text}, {precipitation_status}, and the temperature is {temperature_celsius}°C."

    # Print the insightful statement
    print(insightful_statement)


# text = "Hello, this is an example of text-to-speech synthesis."
tts = gTTS(insightful_statement)
tts.save("output.mp3")  # Save the speech to an audio file

# Load the audio file
pygame.mixer.music.load("output.mp3")

# Play the audio file
pygame.mixer.music.play()

# Block execution until the audio finishes playing
while pygame.mixer.music.get_busy():
    # pygame.time.Clock().tick(1)  # Adjust the tick rate as needed
    pass

# Optionally, you can quit Pygame when done
pygame.quit()
