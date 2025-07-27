import requests
from dotenv import load_dotenv
import os

load_dotenv() #loads variable from .env

api_key = os.getenv("API_KEY")
city = "KOCHI"

url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric" 

#print(response.status_code)
#print(response.json())
#print(response.json().keys())

response= requests.get(url)
data = response.json()

temp=data["main"]["temp"]
description= data["weather"][0]["description"]
city_name = data["name"]

print (f"The weather in {city_name} is {temp} °C with {description}" )