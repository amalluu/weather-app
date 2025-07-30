
import requests
from dotenv import load_dotenv
import os
from flask import Flask , render_template #importing flask and render_template is a function for rendering templates 

load_dotenv()
api_key = os.getenv("API_KEY") #Environment setup should happen before you define routes(web app instance)

app = Flask (__name__)# this creates the web app instance. __name__ refers to the current Python module

@app.route('/')#route which shows the form
def hello():
        return render_template('index.html')

@app.route('/results', methods=['POST'])#processes the form and shows weather #methods=['POST'] allow the route to accept POST requests
def show_results():
    return "Weather results here"
if __name__ =="__main__": #to run the app
    app.run()