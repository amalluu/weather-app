
import requests
from dotenv import load_dotenv
import os
from flask import Flask , render_template ,request, redirect, url_for, jsonify#importing flask # render_template is a function for rendering templates # request imports the 'request' object from the Flask framework
from datetime import datetime
import json

load_dotenv()
api_key = os.getenv("API_KEY") #Environment setup should happen before you define routes(web app instance)

app = Flask (__name__)# this creates the web app instance. __name__ refers to the current Python module


@app.route('/')#route which shows the form
def hello():
        return render_template('index.html')



@app.route('/results', methods=['POST'])#processes the form and shows weather #methods=['POST'] allow the route to accept POST requests
def show_results():
    
    city = request.form.get("cityname")#request.form is a dictionary which contains the submitted form data(only when form method is POST)# .get("cityname")  SIMILAR AS dict.get("key") - MORE SAFE
    clean_city = city.strip()#removes unnecessary spacings that entered

    if not city or city.strip() == "":
        return redirect(url_for('hello'))
        

    data = get_weatherdata(clean_city)
    
    if "error" in data:
        return render_template("results.html",cityy=clean_city,error= data["error"])
    
        
   # Enhanced weather data extraction
    current_temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    description = data["weather"][0]["description"]
    main_weather = data['weather'][0]['main']
    wind_speed = data.get("wind", {}).get("speed", 0)
    visibility = data.get("visibility", 0) / 1000  # Convert to km
    
    # Get additional data
    forecast_data = get_forecast_data(clean_city)
    air_quality = get_air_quality(data["coord"]["lat"], data["coord"]["lon"])
    
    outfit = outfit_recommend(current_temp, description)
    advice = get_weather_advice(current_temp, description, main_weather)


    return render_template("results.html", 
                        cityy=clean_city,
                         temp=current_temp,
                         feels_like=feels_like,
                         humidity=humidity,
                         pressure=pressure,
                         description=description,
                         main_weather=main_weather,
                         wind_speed=wind_speed,
                         visibility=visibility,
                         advice=advice,
                         outfit=outfit,
                         forecast=forecast_data,
                         air_quality=air_quality)

def outfit_recommend(temp,description):
        outfit =" "

        
    # Temperature-based recommendations 
        if temp<0:
           outfit +="Heavy coat, gloves, and scarf needed!🧣<br>Start with a fitted base layer, like a thermal top and leggings🧦<br>Don't forget the boots!!👢"
        elif temp<10:
            outfit +="Wear a warm jacket or layered coat🧥<br>Add a light scarf and gloves🧤<br>A sweater or thermal layer underneath will keep you cozy!<br>Don't forget the boots!!👢"
        elif temp<20:
            outfit +="A light jacket or hoodie should do the trick🧥<br>Layer with a long-sleeve top or sweater👚<br>Keep a scarf handy just in case🧣<br>Comfortable sneakers or shoes will be perfect👟"
        elif temp < 25:
            outfit +="Perfect for a T-shirt or a light full-sleeve top👕<br>Jeans, cotton pants, or skirts work well👖👗<br>Choose your comfy sneakers or sandals👟🩴"
        elif temp < 30:
            outfit +=" Time for light, breathable clothes like cotton T-shirts, tank tops, or dresses👚🩱<br>Stay hydrated and wear sunscreen🧴🕶️<br>Shorts or airy pants are ideal🩳👖<br>Open footwear like sandals or flip-flops will keep you comfy🩴"

        else:
            outfit +="Wear the lightest, most breathable clothes you have — cotton, linen, or dry-fit👕🩳<br>Stay in the shade when possible and drink plenty of water💧<br>Sunglasses, a cap, and sunscreen are a must!🕶️🧢🧴<br>Flip-flops or breathable shoes will keep your feet cool🩴"

    #  Weather condition-based recommendations

        if 'rain' in description or 'drizzle' in description:
         outfit += "Don't forget an umbrella and waterproof jacket!"
        elif "snow" in description:
             outfit+= "Wear waterproof boots and warm gloves!"
        elif "sun" in description:
             outfit+= "Don't forget sunglasses and sunscreen!"        
        return outfit

#weather API call
def get_weatherdata(clean_city):
     
 
        
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={clean_city}&appid={api_key}&units=metric" 
        response= requests.get(url)
        
        if response.status_code ==200:
            return response.json()
        elif response.status_code== 404:
             return {"error":"City not found. Check the spelling and Try Again"}
        else:
             return{"error":"Unable to fetch data, Please try again later."}
        

    except requests.exceptions.RequestException:# catches all networking problems
            return {"error":"Network error. Please check your internet connection"}
    

def get_weather_advice(temp,description):
    advice = " "

    if temp < 5:
          advice+= "🥶 It's quite cold! Stay warm and consider hot drinks."
    elif temp>30:
         advice+= "🌡️ It's hot! Stay hydrated and avoid prolonged sun exposure."
    
    if "rain" in description or "drizzle" in description:
        advice += "🌧️ Rainy weather - perfect for indoor activities!"

    elif "snow" in description:
         advice+=  "❄️ Snowy conditions - drive carefully and stay warm!"   
    elif "thunder" in description:
         advice+= "⚡️ Thunderstorms - Seek shelter in a sturdy building or hardtop car, avoid tall objects and electrical appliances, and stay away from water."
    elif "clear" in description:
         advice+="☀️ perfect for indoor activities! "
    elif " few" in description:
         advice+="☁️  Monitor weather, as conditions can change. Have a light jacket or umbrella just in case"
    elif "scattered" in description:
         advice+="☁️☁️ Remain aware of the weather. Seek shade occasionally and stay hydrated."
    elif "broken" in description:
         advice+= " ☁️☁️ Be prepared for potential changes in weather patterns. Carry rain gear and seek shelter if the clouds darken"
    elif "overcast" in description:
         advice+= "☁️☁️ Enjoy indoor activities. If heading out, dress warmly and bring an umbrella or rain gear"
    
    elif "tornado" in description:
         advice+= "🌪️ Tornado: Seek immediate shelter in a basement or interior room, avoid windows, and protect your head."
    
    else:
         advice += "Have a Great Day!"
    return advice


def get_forecast_data(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            forecast = response.json()
            # Process 5-day forecast
            daily_forecast = []
            hourly_forecast = []
            
            for i in range(0, min(len(forecast["list"]), 40), 8):  # Every 24 hours
                item = forecast["list"][i]
                daily_forecast.append({
                    "day": datetime.fromtimestamp(item["dt"]).strftime("%a"),
                    "temp_max": round(item["main"]["temp_max"]),
                    "temp_min": round(item["main"]["temp_min"]),
                    "description": item["weather"][0]["description"],
                    "main": item["weather"][0]["main"]
                })

              # Get hourly for next 24 hours
            for i in range(min(8, len(forecast["list"]))):
                item = forecast["list"][i]
                hourly_forecast.append({
                    "time": datetime.fromtimestamp(item["dt"]).strftime("%I %p"),
                    "temp": round(item["main"]["temp"]),
                    "main": item["weather"][0]["main"]
                })
            
            return {"daily": daily_forecast, "hourly": hourly_forecast}
    except:
        return {"daily": [], "hourly": []}

def get_air_quality(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            aqi = data["list"][0]["main"]["aqi"]
            aqi_labels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
            return {"aqi": aqi, "label": aqi_labels.get(aqi, "Unknown")}
    except:
        return {"aqi": 1, "label": "Good"}                


if __name__ =="__main__": #to run the app
    app.run(debug=True)

     
         











