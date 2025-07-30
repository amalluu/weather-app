
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

@app.route('/results', methods=['POST'])#processes the form and shows weather #methods=['POST'] allow the route to accept POST requests
def show_results():
    
    city = request.form.get("cityname")#request.form is a dictionary which contains the submitted form data(only when form method is POST)# .get("cityname")  SIMILAR AS dict.get("key") - MORE SAFE
    print(city)
    return f"You searched city for :{city}"
if __name__ =="__main__": #to run the app
    app.run(debug=True)