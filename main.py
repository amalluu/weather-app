import requests
from dotenv import load_dotenv
import os

load_dotenv() #loads variable from .env

api_key = os.getenv("API_KEY")

city = input("Which city would you like weather for?\n")
print(f"City entered: '{city}'")


url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric" 

#print(response.status_code)
#print(response.json())
#print(response.json().keys())

response= requests.get(url)
data = response.json()
#print("API Response:", data)

if data["cod"] == "404":
    print("City not found! Please try again.")
elif data["cod"] == "400":
    print("Please enter a city name!")
else:
    temp=data["main"]["temp"]
    description= data["weather"][0]["description"]
    city_name = data["name"]

    print (f"The weather in {city_name} is {temp} °C with {description}" ) 
