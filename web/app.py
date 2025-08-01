
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
        city_name = data["name"]
        main_weather = data['weather'][0]['main']
        #return f"The weather in {city_name} is {temp}°C with {description}"
    
        return render_template("results.html",city= clean_city,temp= temp, description=description)

if __name__ =="__main__": #to run the app
    app.run(debug=True)