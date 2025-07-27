import requests
from dotenv import load_dotenv
import os

load_dotenv() #loads variable from .env

api_key = os.getenv("API_KEY")


city = input("Which city would you like weather for?\n")
print(f"City entered: '{city}'")
if city.strip() == "":
    print("Please enter a city name!")


else:
    clean_city = city.strip()#removes unnecessary spacings that entered
    url = f"http://api.openweathermap.org/data/2.5/weather?q={clean_city}&appid={api_key}&units=metric" 

#print(response.status_code)
#print(response.json())
#print(response.json().keys())

    response= requests.get(url)
    data = response.json()
#print("API Response:", data)

    if data["cod"] != 200:
        print(f"Error: {data['message']}")
    else:
        temp=data["main"]["temp"]
        description= data["weather"][0]["description"]
        city_name = data["name"]

        print (f"The weather in {city_name} is {temp} °C with {description}" ) 
        if temp<0:
            print("Bundle up!🥶\n Heavy coat, gloves, and scarf needed!🧣\nStart with a fitted base layer, like a thermal top and leggings🧦\nDon't forget the boots!!👢")
        elif 0<temp<=10:
            print("Chilly weather ahead!🌬️\nWear a warm jacket or layered coat🧥\nAdd a light scarf and gloves🧤\nA sweater or thermal layer underneath will keep you cozy!\nDon't forget the boots!!👢")
        elif 10<temp<20:
            print("Cool and comfy! 🍂\nA light jacket or hoodie should do the trick🧥\nLayer with a long-sleeve top or sweater👚\nKeep a scarf handy just in case🧣\nComfortable sneakers or shoes will be perfect👟")
        elif 20 <= temp < 25:
            print("Pleasant weather! 🌤️\nPerfect for a T-shirt or a light full-sleeve top👕\nJeans, cotton pants, or skirts work well👖👗\nChoose your comfy sneakers or sandals👟🩴")
        elif 25 <= temp < 30:
            print("Warm and sunny! ☀️\nTime for light, breathable clothes like cotton T-shirts, tank tops, or dresses👚🩱\nStay hydrated and wear sunscreen🧴🕶️\nShorts or airy pants are ideal🩳👖\nOpen footwear like sandals or flip-flops will keep you comfy🩴")

        else:
            print("It's hot out there! 🔥\nWear the lightest, most breathable clothes you have — cotton, linen, or dry-fit👕🩳\nStay in the shade when possible and drink plenty of water💧\nSunglasses, a cap, and sunscreen are a must!🕶️🧢🧴\nFlip-flops or breathable shoes will keep your feet cool🩴")
    
