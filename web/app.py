
import requests
from dotenv import load_dotenv
import os
from flask import Flask , render_template ,request #importing flask # render_template is a function for rendering templates # request imports the 'request' object from the Flask framework

load_dotenv()
api_key = os.getenv("API_KEY") #Environment setup should happen before you define routes(web app instance)

app = Flask (__name__)# this creates the web app instance. __name__ refers to the current Python module

@app.route('/')#route which shows the form
def hello():
        return render_template('index.html')


#.get() is a safer way to access values from dictionaries
'''data = {"name": "Amalu"}

data.get("name")        # ✅ returns "Amalu"
data.get("age")         # ✅ returns None (no crash)
data.get("age", 0)      # ✅ returns 0 (default)

data["name"]            # ✅ returns "Amalu"
data["age"]             # ❌ KeyError: 'age' '''



@app.route('/results', methods=['POST'])#processes the form and shows weather #methods=['POST'] allow the route to accept POST requests
def show_results():
    
    city = request.form.get("cityname")#request.form is a dictionary which contains the submitted form data(only when form method is POST)# .get("cityname")  SIMILAR AS dict.get("key") - MORE SAFE
    if not city or city.strip() == "":
        return"Please enter a city name!"
        


    else:
        clean_city = city.strip()#removes unnecessary spacings that entered
        url = f"http://api.openweathermap.org/data/2.5/weather?q={clean_city}&appid={api_key}&units=metric" 
        response= requests.get(url)
        data = response.json()
        #return(data)
    

    if data.get("cod") != 200:
        return f"Error: {data.get('message','Unknown error')}"
    else:
        temp=data["main"]["temp"]
        description= data["weather"][0]["description"]
        main_weather = data['weather'][0]['main']
    
        return outfit_recommend(temp,description,main_weather,clean_city)
        #return f"The weather in {city_name} is {temp}°C with {description}"

def outfit_recommend(temp,description,main_weather,clean_city):
        advice =" "

        
        
        if temp<0:
            advice +="Bundle up!🥶\n Heavy coat, gloves, and scarf needed!🧣\nStart with a fitted base layer, like a thermal top and leggings🧦\nDon't forget the boots!!👢"
        elif 0<temp<=10:
            advice +="Chilly weather ahead!🌬️\nWear a warm jacket or layered coat🧥\nAdd a light scarf and gloves🧤\nA sweater or thermal layer underneath will keep you cozy!\nDon't forget the boots!!👢"
        elif 10<temp<20:
            advice +="Cool and comfy! 🍂\nA light jacket or hoodie should do the trick🧥\nLayer with a long-sleeve top or sweater👚\nKeep a scarf handy just in case🧣\nComfortable sneakers or shoes will be perfect👟"
        elif 20 <= temp < 25:
            advice +="Pleasant weather! 🌤️\nPerfect for a T-shirt or a light full-sleeve top👕\nJeans, cotton pants, or skirts work well👖👗\nChoose your comfy sneakers or sandals👟🩴"
        elif 25 <= temp < 30:
            advice +="Warm and sunny! ☀️\n Time for light, breathable clothes like cotton T-shirts, tank tops, or dresses👚🩱\nStay hydrated and wear sunscreen🧴🕶️\nShorts or airy pants are ideal🩳👖\nOpen footwear like sandals or flip-flops will keep you comfy🩴"

        else:
            advice +="It's hot out there! 🔥\nWear the lightest, most breathable clothes you have — cotton, linen, or dry-fit👕🩳\nStay in the shade when possible and drink plenty of water💧\nSunglasses, a cap, and sunscreen are a must!🕶️🧢🧴\nFlip-flops or breathable shoes will keep your feet cool🩴"

        if "heavy" in description:
             for word in ["rain","snow","thunder","drizzle"]:
                  if word in description:
                       advice +=f"⚠️ Heavy {word.capitalize()}! Stay safe."
                       break
                  
        if "light"  in description:
             for word in ["rain","snow","thunder","drizzle"]:
                  if word in description:
                       advice +=f"⚠️ Light {word.capitalize()}! Stay safe."
                       break
                  
        
             
        return render_template("results.html",cityy= clean_city,temp= temp, description=description, advice= advice)

if __name__ =="__main__": #to run the app
    app.run(debug=True)